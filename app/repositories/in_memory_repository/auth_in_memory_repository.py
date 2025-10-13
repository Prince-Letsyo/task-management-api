from fastapi import HTTPException, status
from typing import List
from app.schemas import User, UserCreate
from app.repositories.base_repository import BaseAuthRepository
from app.utils import get_password_hash, verify_password

user_list: List[User] = []


class AuthInMemoryRepository(BaseAuthRepository):
    async def create_user(self, user_create: UserCreate) -> User:
        user_error = await self.get_user_by_username(user_create.username)
        if not isinstance(user_error, User):
            hashed_password = get_password_hash(user_create.password)
            user_create.password = hashed_password
            user = User(id=len(user_list) + 1, **user_create.model_dump())
            user_list.append(user)
            return user
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exist",
        )

    async def authenticate_user(self, username: str, password: str) -> User | str:
        user_error = await self.get_user_by_username(username)
        if isinstance(user_error, str):
            return "Invalid username or password"
        elif isinstance(user_error, User) and verify_password(
            password, user_error.password
        ):
            return user_error
        else:
            return "Invalid username or password"

    async def get_user_by_username(self, username: str) -> User:
        user = next((user for user in user_list if user.username == username), None)
        if isinstance(user, User):
            return user
        return "user does not exist"
