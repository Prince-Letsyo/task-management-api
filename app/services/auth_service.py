from typing import cast
from app.schemas import User, UserCreate, Token, UserBase
from app.repositories.base_repository import BaseAuthRepository
from app.config import config
from app.utils import create_access_token
from datetime import timedelta


class UserResponse(UserBase):
    token: Token


ACCESS_TOKEN_EXPIRE_MINUTES: str | int | bool | None = config.env.get("ACCESS_TOKEN_EXPIRE_MINUTES")


class AuthService:
    def __init__(self, repository: BaseAuthRepository) -> None:
        self.repository: BaseAuthRepository = repository

    async def sign_up(self, user_create: UserCreate) -> UserResponse:
        user: User = await self.repository.create_user(user_create)
        return self.__prepare_token_data(user)

    def __prepare_token_data(self, user: User) -> UserResponse:
        access_token_expires: timedelta = timedelta(
            minutes=float(cast(str, ACCESS_TOKEN_EXPIRE_MINUTES))
        )
        access_token: str = create_access_token(
            data={"username": user.username, "email": user.email},
            expires_delta=access_token_expires,
        )
        return UserResponse(
            username=user.username,
            email=user.email,
            token=Token(access_token=access_token, token_type="Bearer"),
        )

    async def log_in(self, username: str, password: str) -> UserResponse:
        user: User = await self.repository.authenticate_user(
            username=username, password=password
        )
        return self.__prepare_token_data(user)
