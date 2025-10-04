from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import ConfigDict


class TokenBase(SQLModel):
    access_token: str = Field(nullable=False)
    token_type: str = Field(nullable=False)

    model_config = ConfigDict(from_attributes=True)


class TokenModel(TokenBase):
    pass


class TokenError(SQLModel):
    error: str


class TokenData(SQLModel):
    username: Optional[str] = None
    scopes: list[str] = []
    user_id: Optional[int] = None
    exp: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)
