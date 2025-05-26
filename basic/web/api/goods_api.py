from http.client import HTTPException
from typing import List
from fastapi import APIRouter

from service.goods_service import add_goods, get_goods_by_id
from entity.entity import Goods


router = APIRouter()

@router.post("/create", response_model=Goods)
def create_goods(goods: Goods):
    add_goods(goods)
    return goods

@router.get("/query/{goods_id}", response_model=Goods)
def query_goods(goods_id: int):
    goods = get_goods_by_id(goods_id)
    if not goods:
        raise HTTPException(status_code=404, detail="Goods not found")
    return goods

@router.get("/list", response_model=List[Goods])
def list_goods():
    return list_goods()

@router.get("/")
def say_hello():
    return "Hello 商品API"