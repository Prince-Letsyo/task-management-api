from sqlmodel import SQLModel, Field
from typing import Optional, List
from pydantic import ConfigDict


class UserBase(SQLModel):
    username: str = Field(index=True, nullable=False, unique=True)
    email: str = Field(index=True, nullable=False)

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str = Field(nullable=False)
    pass


class UserUpdate(SQLModel):
    username: Optional[str] = Field(default=None, nullable=True)
    email: Optional[str] = Field(default=None, nullable=True)
    password: Optional[str] = Field(default=None, nullable=True)


class UserError(SQLModel):
    error: str

