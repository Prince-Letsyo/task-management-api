from typing import cast, override

from pydantic import EmailStr
from app.core import (
    InvalidUserPasswordException,
    UserDoesnotExistException,
    UserExistException,
)
from app.core.exceptions import UserAccountNotActiveException
from app.schemas import User, UserCreate
from app.repositories.base_repository import BaseAuthRepository
from app.utils import password_validator

users: dict[int, User] = {}


class AuthInMemoryRepository(BaseAuthRepository):
    @override
    async def create_user(self, user_create: UserCreate) -> User:
        try:
            user_exist: User = await self.get_user_by_username(user_create.username)
            if user_exist:
                raise UserExistException("User already exist")
        except Exception:
            user: User = User.model_validate(
                {
                    **user_create.model_dump(),
                    "id": len(users) + 1,
                    "hashed_password": password_validator.get_password_hash(
                        user_create.password
                    ),
                    "is_active": False,
                }
            )
            users[cast(int, user.id)] = user
            return user

    @override
    async def activate_user_account(self, username: str) -> User:
        user: User = await self.get_user_by_username(username=username)
        user.is_active = True
        users[cast(int, user.id)] = user
        return user

    @override
    async def authenticate_user(self, username: str, password: str) -> User:
        try:
            user: User = await self.get_user_by_username(username=username)
            if password_validator.verify_password(
                plain_password=password, hashed_password=user.hashed_password
            ):
                raise InvalidUserPasswordException("Invalid user credentials")
            return user
        except Exception as e:
            raise e

    @override
    async def get_user_by_username(self, username: str) -> User:
        user: User | None = next(
            (user for user in users.values() if user.username == username), None
        )
        if isinstance(user, User):
            if not user.is_active:
                raise UserAccountNotActiveException("User account is not active")
            return user
        raise UserDoesnotExistException("User does not exist")

    @override
    async def get_user_by_email(self, email: EmailStr) -> User:
        user: User | None = next(
            (user for user in users.values() if user.email == email), None
        )
        if isinstance(user, User):
            return user
        raise UserDoesnotExistException("User does not exist")

    @override
    async def update_user_password(self, email: EmailStr, new_password: str) -> User:
        user: User = await self.get_user_by_email(email=email)
        user.hashed_password = password_validator.get_password_hash(new_password)
        users[cast(int, user.id)] = user
        return user