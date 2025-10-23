from sqlalchemy import ScalarResult
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas import User, UserCreate
from app.utils import get_password_hash, verify_password
from app.repositories.base_repository import BaseAuthRepository
from app.exceptions import InvalidUserPasswordException
from typing import override


class AuthSQLRepository(BaseAuthRepository):
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    @override
    async def create_user(self, user_create: UserCreate) -> User:
        user = User.model_validate(
            {
                **user_create.model_dump(),
                "password": get_password_hash(user_create.password),
            }
        )
        try:
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except Exception as e:
            raise e

    @override
    async def authenticate_user(self, username: str, password: str) -> User:
        try:
            user = await self.get_user_by_username(username)
            if not verify_password(password, user.password):
                raise InvalidUserPasswordException("Invalid user credentials")
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
