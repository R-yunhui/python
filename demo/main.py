from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uvicorn

# --- FastAPI 应用实例 ---
app = FastAPI(
    title="我的简单FastAPI学习应用",
    description="这是一个非常基础的FastAPI应用，用于学习核心概念。",
    version="0.1.0"
)

# --- 数据模型 (Pydantic Models) ---
class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tags: List[str] = []

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    name: Optional[str] = None
    price: Optional[float] = None
    tags: Optional[List[str]] = None

class ItemResponse(ItemBase):
    id: int
    created_at: datetime

# --- 模拟数据库 ---
# 使用一个简单的列表来存储数据，方便演示
fake_items_db = []
next_item_id = 1 # 用于生成唯一的物品ID

# --- API 路由 (Endpoints) ---

@app.get("/")
async def read_root():
    """
    根路径，返回一个欢迎信息。
    """
    return {"message": "欢迎使用我的简单FastAPI应用!"}

@app.post("/items/", response_model=ItemResponse, status_code=201)
async def create_item(item: ItemCreate):
    """
    创建一个新的物品。
    - 请求体需要包含 `name` 和 `price`。
    - `description` 和 `tags` 是可选的。
    """
    global next_item_id
    new_item_data = item.model_dump()
    new_item = ItemResponse(
        id=next_item_id,
        created_at=datetime.now(),
        **new_item_data
    )
    fake_items_db.append(new_item)
    next_item_id += 1
    return new_item

@app.get("/items/", response_model=List[ItemResponse])
async def read_items(skip: int = 0, limit: int = 10):
    """
    获取物品列表。
    - 支持通过 `skip` 和 `limit` 参数进行分页。
    """
    return fake_items_db[skip : skip + limit]

@app.get("/items/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int):
    """
    根据物品ID获取单个物品的详细信息。
    - 如果物品不存在，返回404错误。
    """
    for item_in_db in fake_items_db:
        if item_in_db.id == item_id:
            return item_in_db
    raise HTTPException(status_code=404, detail=f"ID为 {item_id} 的物品未找到")

@app.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, item_update_data: ItemUpdate):
    """
    更新指定ID的物品信息。
    - 请求体中可以包含部分或全部可更新字段。
    - 如果物品不存在，返回404错误。
    """
    for index, item_in_db in enumerate(fake_items_db):
        if item_in_db.id == item_id:
            # Pydantic v2: model_dump(exclude_unset=True) 
            # 只获取显式设置的字段进行更新
            update_data = item_update_data.model_dump(exclude_unset=True) 
            
            updated_item = item_in_db.model_copy(update=update_data)
            fake_items_db[index] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail=f"ID为 {item_id} 的物品未找到，无法更新")

@app.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int):
    """
    根据物品ID删除一个物品。
    - 如果物品不存在，返回404错误。
    - 成功删除后，返回204 No Content状态码。
    """
    for index, item_in_db in enumerate(fake_items_db):
        if item_in_db.id == item_id:
            fake_items_db.pop(index)
            return # 对于204，FastAPI不应返回任何内容
    raise HTTPException(status_code=404, detail=f"ID为 {item_id} 的物品未找到，无法删除")

# --- 运行应用 ---
# 可以通过命令行 `uvicorn main:app --reload` 来启动
# 或者直接运行此脚本 `python main.py`
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)