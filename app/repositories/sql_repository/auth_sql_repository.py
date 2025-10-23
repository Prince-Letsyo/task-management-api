from sqlalchemy import ScalarResult
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas import User, UserCreate
from app.utils import get_password_hash, verify_password
from app.repositories.base_repository import BaseAuthRepository
from app.core import AppException, ConflictException
from typing import override


class AuthSQLRepository(BaseAuthRepository):
    def __init__(self, db: AsyncSession) -> None:
        self.db: AsyncSession = db

    @override
    async def create_user(self, user_create: UserCreate) -> User:
        user: User = User.model_validate(
            {
                **user_create.model_dump(),
                "password": get_password_hash(user_create.password),
            }
        )
        try:
            self.db.add(instance=user)
            await self.db.commit()
            await self.db.refresh(instance=user)
            return user
        except IntegrityError as e:
            raise ConflictException(
                message="Task must be unique",
            )
        except Exception as e:
            raise e

    @override
    async def authenticate_user(self, username: str, password: str) -> User:
        try:
            user: User = await self.get_user_by_username(username)
            if not verify_password(plain_password=password, hashed_password=  user.password):
                raise AppException(message="Invalid user credentials")
            return user
        except Exception as e:
            raise e

    @override
    async def get_user_by_username(self, username: str) -> User:
        try:
            result: ScalarResult[User] = await self.db.exec(
                select(User).where(User.username == username)
            )
            return result.one()
        except Exception as e:
            raise e
