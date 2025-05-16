# 简单FastAPI学习项目

这是一个非常基础的FastAPI应用，用于学习FastAPI的核心概念。

## 功能

- **创建物品 (POST /items/)**: 添加新的物品到列表。
- **读取物品列表 (GET /items/)**: 获取所有物品，支持分页。
- **读取单个物品 (GET /items/{item_id})**: 根据ID获取特定物品。
- **更新物品 (PUT /items/{item_id})**: 更新现有物品的信息。
- **删除物品 (DELETE /items/{item_id})**: 根据ID删除物品。

## 如何运行

1.  **创建并激活虚拟环境 (推荐)**:
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # macOS/Linux
    source .venv/bin/activate
    ```

2.  **安装依赖**: 
    确保你的 `requirements.txt` 文件包含以下内容:
    ```txt
    fastapi>=0.104.1,<0.110.0
    uvicorn[standard]>=0.23.2,<0.24.0
    ```
    然后运行:
    ```bash
    pip install -r requirements.txt
    ```

3.  **启动应用服务**:
    你可以直接运行 `main.py` 文件:
    ```bash
    python main.py
    ```
    或者使用 Uvicorn 命令 (更推荐的方式，特别是在开发时，因为它支持自动重载):
    ```bash
    uvicorn main:app --reload
    ```

4.  **访问API文档**:
    应用启动后，你可以在浏览器中访问自动生成的API文档：
    - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
    - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 代码结构

- `main.py`: 包含所有的FastAPI应用逻辑、数据模型和API路由。
- `requirements.txt`: 列出项目所需的Python包。

这个项目特意保持简单，以便于理解FastAPI的基本用法，包括路径操作、请求体验证、响应模型和错误处理。 