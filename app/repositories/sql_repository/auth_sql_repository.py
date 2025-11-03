from pydantic import EmailStr
from sqlalchemy import ScalarResult
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas import User, UserCreate
from app.utils import password_validator
from app.repositories.base_repository import BaseAuthRepository
from app.core import AppException, ConflictException, NotFoundException
from typing import override


class AuthSQLRepository(BaseAuthRepository):
    def __init__(self, db: AsyncSession) -> None:
        self.db: AsyncSession = db

    @override
    async def create_user(self, user_create: UserCreate) -> User:
        try:
            user: User = User.model_validate(
                obj={
                    **user_create.model_dump(),
                    "hashed_password": password_validator.get_password_hash(
                        user_create.password
                    ),
                }
            )
            self.db.add(instance=user)
            await self.db.commit()
            await self.db.refresh(instance=user)
            return user
        except IntegrityError as e:
            raise ConflictException(
                message="User already exist",
            )
        except Exception as e:
            raise e

    @override
    async def activate_user_account(self, username: str) -> User:
        try:
            result: ScalarResult[User] = await self.db.exec(
                select(User).where(User.username == username)
            )
            user: User = result.one()
            if user.is_active: 
                raise AppException(message="User account is already active.")
            user.is_active = True
            self.db.add(instance=user)
            await self.db.commit()
            await self.db.refresh(instance=user)
            return user
        except NoResultFound as e:
            raise NotFoundException(
                message=f"User with username '{username}' does not exist",
            )
        except Exception as e:
            raise e

    @override
    async def authenticate_user(self, username: str, password: str) -> User:
        try:
            user: User = await self.get_user_by_username(username)
            if not password_validator.verify_password(
                plain_password=password, hashed_password=user.hashed_password
            ):
                raise AppException(message="Incorrect username or password")
            return user
        except Exception as e:
            raise e

    @override
    async def get_user_by_username(self, username: str) -> User:
        try:
            result: ScalarResult[User] = await self.db.exec(
                select(User).where(User.username == username)
            )
            user = result.one()
            if user.is_active is False:
                raise AppException(message="User account is not active")
            return user

        except NoResultFound as e:
            raise NotFoundException(
                message=f"Incorrect username or password",
            )
        except Exception as e:
            raise e

    @override
    async def get_user_by_email(self, email: EmailStr) -> User:
        try:
            result: ScalarResult[User] = await self.db.exec(
                select(User).where(User.email == email)
            )
            return result.one()

        except NoResultFound as e:
            raise NotFoundException(
                message=f"Incorrect username or password",
            )
        except Exception as e:
            raise e

    @override
    async def update_user_password(self, email: EmailStr, new_password: str) -> User:
        try:
            user: User = await self.get_user_by_email(email=email)
            user.hashed_password = password_validator.get_password_hash(new_password)
            self.db.add(instance=user)
            await self.db.commit()
            await self.db.refresh(instance=user)
            return user
        except NoResultFound as e:
            raise NotFoundException(
                message=f"User with email '{email}' does not exist",
            )
        except Exception as e:
            raise e
