# 模拟数据库存储
from typing import List, Optional

from entity.entity import Goods

# 用内存模拟数据库
_fake_db = List[Goods]

def add_goods(goods: Goods) -> None:
    _fake_db.append(goods)
    
def get_goods_by_id(goods_id: int) -> Optional[Goods]:
    for goods in _fake_db:
        if goods.id == goods_id:
            return goods
    return None

def list_goods() -> List[Goods]:
    return _fake_db

