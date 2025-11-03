from .auth import (
    password_validator,
    jwt_auth_token,
    JWTPayload,
)
from .alembic_utils import upgrade_database, downgrade_database
from .email import email_service, EmailService
from .logging import main_logger, filter_sensitive
from urllib.parse import urlparse

def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([
            result.scheme,   # http, https, ftp, etc.
            result.netloc,   # domain present
        ])
    except:
        return False


__all__ = [
    "password_validator",
    "jwt_auth_token",
    "email_service",
    "EmailService",
    "main_logger",
    "filter_sensitive",
    "JWTPayload",
    "upgrade_database",
    "downgrade_database",
]
