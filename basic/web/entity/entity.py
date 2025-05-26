from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: Optional[int] = None
    name : Optional[str] = None
    email : Optional[str] = None
    
class Goods(BaseModel):
    id: Optional[int] = None
    name : Optional[str] = None
    price : Optional[float] = None
    inventory : Optional[int] = None
