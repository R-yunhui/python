import langchain
# langchain.debug = True  # debug 打印详细的日志

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain.agents import initialize_agent, AgentType
import json

# 1. 定义一个示例工具
@tool
def get_current_weather(location: str, unit: str = "celsius") -> str:
    """获取指定地点的当前天气信息。"""
    if "beijing" in location.lower() or "北京" in location:
        return json.dumps({"location": location, "temperature": "10", "unit": unit, "description": "晴朗"})
    elif "shanghai" in location.lower() or "上海" in location:
        return json.dumps({"location": location, "temperature": "15", "unit": unit, "description": "多云"})
    else:
        return json.dumps({"location": location, "temperature": "unknown", "description": "未知天气"})

def mcp_style_llm_call():
    # 初始化 LLM
    llm = ChatOpenAI(
        model="qwen2.5-vl-72b-instruct",
        api_key="NA",
        base_url="http://192.168.2.54:9015/v1/",  # 你的本地服务地址
        max_retries=3,
        temperature=0.7,
        timeout=20
    )

    # 初始化 Agent
    agent = initialize_agent(
        tools=[get_current_weather],
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,  # 关键，自动工具调用
        verbose=True  # 打印详细推理过程，调试时可用
    )

    print("请输入您的问题，例如：'北京现在天气怎么样？' 或 '上海的天气如何？'（输入 'exit' 退出）")
    while True:
        user_prompt = input("用户: ")
        if user_prompt.lower() == 'exit':
            print("程序退出。")
            break
        try:
            response = agent.invoke(user_prompt)
            print(f"模型回复: {response['output']}")
        except Exception as e:
            print(f"发生错误: {e}")

if __name__ == "__main__":
    mcp_style_llm_call()
    
    
    
    
