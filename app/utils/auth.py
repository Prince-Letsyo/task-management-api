from datetime import timedelta, datetime, timezone
from jose import jwt
from pwdlib import PasswordHash
from app.config import config
from typing import Any, TypedDict, cast

SECRET_KEY: str | int | bool | None = config.env.get("SECRET_KEY")
ALGORITHM: str | int | bool | None = config.env.get("ALGORITHM")

password_hash = PasswordHash.recommended()


def verify_password(plain_password: str | bytes, hashed_password: str | bytes) -> bool:
    return password_hash.verify(password=plain_password, hash=hashed_password)


def get_password_hash(password: str | bytes) -> str:
    return password_hash.hash(password)


class JWTPayload(TypedDict):
    username: str
    email: str


class JWTPayloadWithExp(JWTPayload):
    exp: datetime


def create_access_token(
    data: JWTPayload, expires_delta: timedelta | None = None
) -> str:
    to_encode: JWTPayload = data.copy()
    if expires_delta:
        expire: datetime = datetime.now(timezone.utc) + expires_delta  # pyright: ignore[reportRedeclaration]
    else:
        expire: datetime = datetime.now(timezone.utc) + timedelta(minutes=15)
    claims: JWTPayloadWithExp = cast(JWTPayloadWithExp, to_encode)
    claims.update({"exp": expire})
    encoded_jwt = jwt.encode(
        claims=dict(claims), key=cast(str, SECRET_KEY), algorithm=cast(str, ALGORITHM)
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict[str, str]:
    try:
        payload: dict[str, Any] = jwt.decode(  # pyright: ignore[reportExplicitAny]
            token, cast(str, SECRET_KEY), algorithms=[cast(str, ALGORITHM)]
        )
        return payload
    except Exception as e:
        raise e
