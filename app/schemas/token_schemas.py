from sqlmodel import SQLModel, Field
from pydantic import ConfigDict


class TokenBase(SQLModel):
    access_token: str = Field(nullable=False)
    token_type: str = Field(nullable=False)

    model_config: ConfigDict = ConfigDict(from_attributes=True)  # pyright: ignore[reportIncompatibleVariableOverride]


class TokenModel(TokenBase):
    pass


class TokenError(SQLModel):
    error: str


class TokenData(SQLModel):
    username: str | None = None
    scopes: list[str] = []
    user_id: int | None = None
    exp: int | None = None
    model_config: ConfigDict = ConfigDict(from_attributes=True)  # pyright: ignore[reportIncompatibleVariableOverride]
