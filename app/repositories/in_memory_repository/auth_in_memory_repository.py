from typing import override
from app.core import (
    InvalidUserPasswordException,
    UserDoesnotExistException,
    UserExistException,
)
from app.schemas import User, UserCreate
from app.repositories.base_repository import BaseAuthRepository
from app.utils import get_password_hash, verify_password

user_list: list[User] = []


class AuthInMemoryRepository(BaseAuthRepository):
    @override
    async def create_user(self, user_create: UserCreate) -> User:
        try:
            user:User = await self.get_user_by_username(user_create.username)
            if user:
                raise UserExistException("User already exist")
        except Exception:
            hashed_password = get_password_hash(user_create.password)
            user_create.password = hashed_password
            user = User.model_validate(
                {
                    **user_create.model_dump(),
                    "password": get_password_hash(user_create.password),
                    "id": len(user_list) + 1,
                }
            )
            user_list.append(user)
        return user

    @override
    async def authenticate_user(self, username: str, password: str) -> User:
        try:
            user:User = await self.get_user_by_username(username=username)
            if verify_password(plain_password=password, hashed_password=user.password):
                raise InvalidUserPasswordException("Invalid user credentials")
            return user
        except Exception as e:
            raise e

    @override
    async def get_user_by_username(self, username: str) -> User:
        user:User|None = next((user for user in user_list if user.username == username), None)
        if isinstance(user, User):
            return user
        raise UserDoesnotExistException("User does not exist")
