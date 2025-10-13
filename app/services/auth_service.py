from app.schemas import User, UserCreate, Token, UserBase
from app.repositories.base_repository import BaseAuthRepository
from app.config import config
from app.utils import create_access_token
from datetime import timedelta
from fastapi import HTTPException, status


class UserResponse(UserBase):
    token: Token


ACCESS_TOKEN_EXPIRE_MINUTES = config.env.get("ACCESS_TOKEN_EXPIRE_MINUTES")


class AuthService:
    def __init__(self, repository: BaseAuthRepository):
        self.repository: BaseAuthRepository = repository

    async def sign_up(self, user_create: UserCreate) -> UserResponse:
        user = await self.repository.create_user(user_create)
        if not user:
            raise HTTPException(status_code=400, detail="User already exists")
        return self.__prepare_token_data(user)

    def __prepare_token_data(self, user: User) -> UserResponse:
        access_token_expires = timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES))
        access_token = create_access_token(
            data={"username": user.username, "email": user.email},
            expires_delta=access_token_expires,
        )
        return UserResponse(
            username=user.username,
            email=user.email,
            token=Token(access_token=access_token, token_type="Bearer"),
        )

    async def log_in(self, username: str, password: str) -> UserResponse:
        user = await self.repository.authenticate_user(username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return self.__prepare_token_data(user)
