import json
import dashscope
import uvicorn
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from uuid import uuid4
from enum import Enum

# LangChain 相关导入
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

from dashscope import ImageSynthesis
from http import HTTPStatus

app = FastAPI(title="LLM模型选择与推理API")

# 允许跨域，方便前端本地开发
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件（前端页面）
app.mount("/web", StaticFiles(directory="llm/web", html=True), name="web")

api_key = "sk-dbc8ed51cec741d388e0ca023d33b551"


# --- 模型类型枚举 ---
class ModelTypeEnum(str, Enum):
    chat = 'chat'
    text2img = 'text2img'
    embedding = 'embedding'  # 如需可解开

# --- 模型配置 ---
class ModelConfig(BaseModel):
    id: str
    model_name: str
    base_url: str
    api_key: str
    model_type: str

# 你可以在这里添加/修改模型
MODEL_LIST = [
    ModelConfig(id="1", model_name="qwen-plus",
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions", api_key=api_key,
                model_type=ModelTypeEnum.chat.value),
    ModelConfig(id="2", model_name="wanx2.1-t2i-turbo",
                base_url="https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis",
                api_key=api_key, model_type=ModelTypeEnum.text2img.value),
    ModelConfig(id="3", model_name="multimodal-embedding-v1",
                base_url="https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding",
                api_key=api_key, model_type=ModelTypeEnum.embedding.value),
]

# 用 session_id 做内存隔离
MEMORY_POOL = {}

# --- API ---
@app.get("/api/models", response_model=List[ModelConfig])
def get_models():
    """获取所有可用模型列表"""
    # FastAPI/Pydantic 会自动将枚举转为字符串
    return MODEL_LIST

@app.get("/")
def root():
    return RedirectResponse(url="/web/")

@app.post("/api/infer")
async def infer(
        model_id: str = Form(...),
        input_text: Optional[str] = Form(None),
        session_id: Optional[str] = Form(None)
):
    """根据模型类型和输入调用真实大模型（langchain），支持简单上下文记忆和文生图"""
    model = next((m for m in MODEL_LIST if m.id == model_id), None)
    if not model:
        return {"error": "模型不存在"}
    # 统一为字符串进行比对
    model_type = str(model.model_type) if not isinstance(model.model_type, str) else model.model_type
    if model_type == ModelTypeEnum.chat.value:
        if not session_id:
            session_id = str(uuid4())
        # 获取/创建 memory
        if session_id not in MEMORY_POOL:
            MEMORY_POOL[session_id] = ConversationBufferMemory(return_messages=True)
        memory = MEMORY_POOL[session_id]

        # 构建 LLMChain
        llm = ChatOpenAI(
            model=model.model_name,
            base_url=model.base_url,
            api_key=Optional[model.api_key],
            temperature=0.5,
            max_tokens=1000,
            timeout=20,
            max_retries=3,
        )

        conversation = ConversationChain(
            llm=llm,
            memory=memory,
            verbose=False
        )

        # 进行对话
        result = conversation.predict(input=input_text)
        return {"result": result, "session_id": session_id}
    elif model_type == ModelTypeEnum.text2img.value:
        if not session_id:
            session_id = str(uuid4())
        # 构造请求
        rsp = ImageSynthesis.call(
            api_key=api_key,
            model=model.model_name,
            prompt=input_text,
            n=1,
            size='1024*1024'
        )
        if rsp.status_code == HTTPStatus.OK:
            # 直接返回第一个图片的URL
            if rsp.output and rsp.output.results and len(rsp.output.results) > 0:
                first_result = next(iter(rsp.output.results), None)
                if first_result:
                    image_url = first_result.url
                    return {"image_url": image_url, "session_id": session_id}
            return {"error": "未获取到图片URL", "session_id": session_id}
        else:
            return {
                "error": f"图片生成失败, status_code: {rsp.status_code}, code: {getattr(rsp, 'code', '')}, message: {getattr(rsp, 'message', '')}",
                "session_id": session_id}
    elif model_type == ModelTypeEnum.embedding.value:
        if not session_id:
            session_id = str(uuid4())
        # 构造请求
        text = input_text
        input_content = [{'text': text}]
        # 调用模型接口
        resp = dashscope.MultiModalEmbedding.call(
            model="multimodal-embedding-v1",
            input=input_content,
            api_key=api_key
        )

        if resp.status_code == HTTPStatus.OK:
            return resp.output['embeddings']
        else:
            return {
                "error": f"embedding 失败, status_code: {resp.status_code}, code: {getattr(resp, 'code', '')}, message: {getattr(resp, 'message', '')}",
                "session_id": session_id}
    else:
        return {"error": "暂不支持的模型类型"}

# 可以通过命令行 `uvicorn api:app --reload` 来启动
# 或者直接运行此脚本 `python api.py`
if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8080, reload=True)
