import jwt
from app.schemas import User, UserCreate, Token, UserBase
from app.repositories.base_repository import BaseAuthRepository
from app.utils import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from datetime import timedelta, datetime, timedelta, timezone
from fastapi import HTTPException, status


class UserResponse(UserBase):
    token: Token


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
            data={"sub": {"username": user.username, "email": user.email}},
            expires_delta=access_token_expires,
        )
        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            token=Token(access_token=access_token, token_type="bearer"),
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


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
