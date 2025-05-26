from fastapi import APIRouter, HTTPException
from typing import List

from entity.entity import User
from service.service import add_user, get_user_by_id, list_users

router = APIRouter()

@router.post("/users", response_model=User)
def create_user(user: User):
    if get_user_by_id(user.id):
        raise HTTPException(status_code=400, detail="User already exists")
    add_user(user)
    return user

@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users", response_model=List[User])
def read_users():
    return list_users()

@router.get("/")
def say_hello():
    return "Hello World！"