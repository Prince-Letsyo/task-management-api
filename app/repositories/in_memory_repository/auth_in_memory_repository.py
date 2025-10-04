import asyncio
from app.schemas import User, UserCreate
from app.repositories.base_repository import BaseAuthRepository
from typing import List
from app.utils import get_password_hash, verify_password

user_list: List[User] = []
user_list_lock = asyncio.Lock()


class AuthInMemoryRepository(BaseAuthRepository):
    async def create_user(self, user_create: UserCreate) -> User:
        async with user_list_lock:
            hashed_password = get_password_hash(user_create.password)
            user_create.password = hashed_password
            user = User(id=len(user_list) + 1, **user_create.model_dump())
            user_list.append(user)
            return user

    async def authenticate_user(self, username: str, password: str) -> User | None:
        async with user_list_lock:
            user = next((user for user in user_list if user.username == username), None)
            if not user:
                return None
            if not verify_password(password, user.password):
                return None
            return user

    async def get_user_by_username(self, username: str) -> User | None:
        async with user_list_lock:
            user = next((user for user in user_list if user.username == username), None)
            return user