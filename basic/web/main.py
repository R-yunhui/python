from fastapi import FastAPI

# 如果是 main.py 在同一个目录下，可以这样导入，如何在外层，需要用全路径（必须在“包的根目录”之外运行你的 Python 程序）
from api.user_api import router as user_router
from api.goods_api import router as goods_router
import uvicorn

app = FastAPI(
    title="简单FastAPI学习应用",
    description="基础的FastAPI应用",
    version="1.0.0"
)

app.include_router(user_router, prefix="/users")
app.include_router(goods_router, prefix="/goods")

# --- 运行应用 ---
# 可以通过命令行 `uvicorn main:app --reload` 来启动
# 或者直接运行此脚本 `python main.py`
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)