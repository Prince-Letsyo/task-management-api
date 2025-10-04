import os
from dotenv import load_dotenv


load_dotenv()

# Default to SQLite; override with DATABASE_URL for production (e.g., PostgreSQL)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./database.db")
# Default to SQLite; override with DATABASE_URL for production (e.g., PostgreSQL)
SQLALCHEMY_TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL", "sqlite+aiosqlite:///./test.db"
)
SECRET_KEY = os.getenv(
    "SECRET_KEY", "c54e0c022aee46c6fd4c606dd133a3a30e36dcea7ce79107e85b99a248885d81"
)
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
ENV_MODE = os.getenv("ENV_MODE", "dev")