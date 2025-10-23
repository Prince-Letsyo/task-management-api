from typing import TypedDict, cast
import pytest_asyncio
from faker import Faker
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from unittest.mock import AsyncMock, Mock

from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.db import AsyncSessionLocal
from app.config import config
from app.schemas.task_schemas import TaskStatus

# Create async engine
test_engine = create_async_engine(cast(str, config.database.get("url")), echo=False)

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
async def task_mock_session():
    session = Mock(spec=AsyncSession)
    session.add = Mock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.get = AsyncMock()
    session.exec = AsyncMock()
    return session


@pytest_asyncio.fixture
async def auth_mock_session():
    session = Mock(spec=AsyncSession)
    session.add = Mock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.get = AsyncMock()
    session.exec = AsyncMock()
    return session


@pytest_asyncio.fixture
async def faker_session() -> Faker:
    # Create a Faker instance with a fixed seed for reproducible data
    faker = Faker()
    faker.seed_instance(1234)  # Fixed seed for reproducibility
    return faker


class TaskTyped(TypedDict):
    id: int
    title: str
    description: str
    status: TaskStatus


@pytest_asyncio.fixture
async def mock_task(faker_session: Faker):
    # Generate dummy task data
    return {
        "id": faker_session.random_int(min=1, max=1000),
        "title": faker_session.sentence(nb_words=5),
        "description": faker_session.paragraph(nb_sentences=2),
        "status": faker_session.random_element(
            elements=("pending", "in-progress", "completed")
        ),
    }


class UserTyped(TypedDict):
    id: int
    username: str
    email: str
    password: str


@pytest_asyncio.fixture
async def mock_user(faker_session: Faker):
    # Generate dummy user data
    return {
        "id": faker_session.random_int(min=1, max=1000),
        "username": faker_session.user_name(),
        "email": faker_session.email(),
        "password": faker_session.password(length=10),
    }
