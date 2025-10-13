from datetime import timedelta, datetime, timezone
from fastapi import HTTPException, status
from pwdlib import PasswordHash
from jose import jwt, JWTError
from app.config import config

ACCESS_TOKEN_EXPIRE_MINUTES = config.env.get("ACCESS_TOKEN_EXPIRE_MINUTES")
SECRET_KEY = config.env.get("SECRET_KEY")
ALGORITHM = config.env.get("ALGORITHM")

password_hash = PasswordHash.recommended()


def verify_password(plain_password: str | bytes, hashed_password: str | bytes) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str | bytes) -> str:
    return password_hash.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
