import os
import pytest
import pytest_asyncio
from dotenv import load_dotenv
from sqlmodel import SQLModel
from app.config.db import AsyncSessionLocal
from sqlalchemy.ext.asyncio import create_async_engine
from unittest.mock import AsyncMock, Mock
from sqlalchemy.ext.asyncio import AsyncSession

load_dotenv()

# Default to SQLite; override with DATABASE_URL for production (e.g., PostgreSQL)
SQLALCHEMY_TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL", "sqlite+aiosqlite:///./test.db"
)

# Create async engine
test_engine = create_async_engine(SQLALCHEMY_TEST_DATABASE_URL, echo=False)

AsyncSessionLocal.configure(bind=test_engine)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def session():
    async with AsyncSessionLocal() as session:
        yield session
        # Rollback any uncommitted changes to ensure clean state
        await session.rollback()
        await session.close()


@pytest_asyncio.fixture
async def mock_session():
    session = Mock(spec=AsyncSession)
    session.add = Mock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.get = AsyncMock()
    session.exec = AsyncMock()
    return session
