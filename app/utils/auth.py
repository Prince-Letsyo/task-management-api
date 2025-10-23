from datetime import timedelta, datetime, timezone
from jose import jwt
from pwdlib import PasswordHash
from app.config import config
from typing import TypedDict, cast

SECRET_KEY = config.env.get("SECRET_KEY")
ALGORITHM = config.env.get("ALGORITHM")

password_hash = PasswordHash.recommended()


def verify_password(plain_password: str | bytes, hashed_password: str | bytes) -> bool:
    return password_hash.verify(plain_password, hashed_password)


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
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    claims = cast(JWTPayloadWithExp, to_encode)
    claims.update({"exp": expire})
    encoded_jwt = jwt.encode(
        dict(claims), cast(str, SECRET_KEY), algorithm=cast(str, ALGORITHM)
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict[str, str]:
    try:
        payload = jwt.decode(
            token, cast(str, SECRET_KEY), algorithms=[cast(str, ALGORITHM)]
        )
        return payload
    except Exception as e:
        raise e
