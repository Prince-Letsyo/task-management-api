from sqlmodel import SQLModel, Field
from typing import Optional, List
from pydantic import ConfigDict, EmailStr


class UserBase(SQLModel):
    username: str = Field(index=True, nullable=False, unique=True)
    email: EmailStr = Field(index=True, nullable=False)

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str = Field(nullable=False, min_length=8)
    pass


class UserUpdate(UserCreate):
    pass


class UserError(SQLModel):
    error: str
