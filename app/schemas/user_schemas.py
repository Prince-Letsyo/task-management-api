from typing import Any, cast
from sqlmodel import SQLModel, Field
from pydantic import ConfigDict, EmailStr, ValidationInfo, field_validator

from app.utils import password_validator


class UserBase(SQLModel):
    username: str = Field(index=True, nullable=False, unique=True)
    email: EmailStr = Field(index=True, nullable=False)

    model_config: ConfigDict = (  # pyright: ignore[reportIncompatibleVariableOverride]
        ConfigDict(from_attributes=True)
    )


class UserCreate(UserBase):
    password: str = Field(nullable=False, min_length=8)

    @field_validator("password")
    @classmethod
    def validate_full_password(cls, v: str, info: ValidationInfo) -> str:
        """Validate password strength and similarity"""
        values: dict[str, Any] = info.data  # pyright: ignore[reportExplicitAny]
        username: str | None = values.get("username")
        email: EmailStr | None = values.get("email")

        if not all([username, email]):
            validation: dict[str, Any] = ( #pyright: ignore[reportExplicitAny, reportRedeclaration]
                password_validator.validate_password(  
                    password=v, username="", email=""
                )
            )
            if not validation["is_valid"]:
                raise ValueError(validation["errors"][0])  # pyright: ignore[reportAny]
            return v

        validation: dict[str, Any] = (  # pyright: ignore[reportExplicitAny]
            password_validator.validate_password(
                password=v, username=cast(str, username), email=cast(str, email)
            )
        )
        if not validation["is_valid"]:
            raise ValueError(
                "; ".join(validation["errors"])  # pyright: ignore[reportAny]
            )
        return v


class UserUpdate(UserCreate):
    pass


class UserError(SQLModel):
    error: str


class AuthLogin(SQLModel):
    username: str = Field(index=True, nullable=False, unique=True)
    password: str = Field(nullable=False, min_length=8)
    model_config: ConfigDict = (  # pyright: ignore[reportIncompatibleVariableOverride]
        ConfigDict(from_attributes=True)
    )
