from typing import List, Optional

from entity.entity import User

# 用内存模拟数据库
_fake_db: List[User] = []

def add_user(user: User) -> None:
    _fake_db.append(user)

def get_user_by_id(user_id: int) -> Optional[User]:
    for user in _fake_db:
        if user.id == user_id:
            return user
    return None

def list_users() -> List[User]:
    return _fake_db