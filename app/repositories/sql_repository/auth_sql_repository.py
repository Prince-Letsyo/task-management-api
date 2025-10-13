from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import (
    IntegrityError,
    OperationalError,
    DataError,
    ProgrammingError,
    SQLAlchemyError,
)
from app.schemas import User, UserCreate
from app.utils import get_password_hash, verify_password
from app.repositories.base_repository import BaseAuthRepository


class AuthSQLRepository(BaseAuthRepository):
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def create_user(self, user_create: UserCreate) -> User:
        user = User(
            username=user_create.username,
            email=user_create.email,
            password=get_password_hash(user_create.password),
        )
        try:
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except Exception as e:
            await self.db.rollback()
            return None

    async def authenticate_user(self, username: str, password: str) -> User:
        user = await self.get_user_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    async def get_user_by_username(self, username: str) -> User:
        query = await self.db.exec(
            User.__table__.select().where(User.username == username)
        )
        return query.first()
