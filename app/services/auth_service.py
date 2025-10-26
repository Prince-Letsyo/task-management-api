from typing import cast
from jose import ExpiredSignatureError, JWTError
from app.core.exceptions import  UnauthorizedException
from app.schemas import AccessToken, RefreshToken, User, UserCreate, Token, UserBase
from app.repositories.base_repository import BaseAuthRepository
from app.utils import jwt_auth_token


class UserResponse(UserBase):
    token: Token


class AuthService:
    def __init__(self, repository: BaseAuthRepository) -> None:
        self.repository: BaseAuthRepository = repository

    async def sign_up(self, user_create: UserCreate) -> UserResponse:
        user: User = await self.repository.create_user(user_create)
        return self.__prepare_token_data(user)

    def __prepare_token_data(self, user: User) -> UserResponse:
        access_token, access_timestamp = jwt_auth_token.access_token(
            data={"username": user.username, "email": user.email},
        )
        refresh_token, refresh_timestamp = jwt_auth_token.refresh_token(
            data={"username": user.username, "email": user.email},
        )
        return UserResponse(
            username=user.username,
            email=user.email,
            token=Token(
                access_token=AccessToken.model_validate(
                    {"token": access_token, "duration": access_timestamp}
                ),
                refresh_token=RefreshToken.model_validate(
                    {"token": refresh_token, "duration": refresh_timestamp}
                ),
            ),
        )

    async def log_in(self, username: str, password: str) -> UserResponse:
        user: User = await self.repository.authenticate_user(
            username=username, password=password
        )
        return self.__prepare_token_data(user)

    async def get_access_token(self, token_string: str):
        try:
            payload: dict[str, str] = jwt_auth_token.decode_token(token_string)
            if payload:
                access_token, access_timestamp = jwt_auth_token.access_token(
                    data={
                        "username": cast(str, payload.get("username")),
                        "email": cast(str, payload.get("email")),
                    },
                )
                return AccessToken.model_validate(
                    {"token": access_token, "duration": access_timestamp}
                )
        except ExpiredSignatureError:
            raise UnauthorizedException(
                message="Token has expired",
            )
        except JWTError:
            raise UnauthorizedException(message="Invalid token")
