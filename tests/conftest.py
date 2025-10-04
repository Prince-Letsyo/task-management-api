import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock, Mock


@pytest_asyncio.fixture(scope="function")
async def session():
    session = Mock(spec=AsyncSession)
    # Existing mocked methods
    session.add = Mock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.get = AsyncMock()
    session.exec = AsyncMock()
    session.delete = AsyncMock()
    session.execute = AsyncMock()
    # Additional mocked methods
    session.flush = AsyncMock()
    session.merge = AsyncMock()
    session.scalar = AsyncMock()
    session.scalars = AsyncMock()
    session.add_all = Mock()
    session.rollback = AsyncMock()
    session.close = AsyncMock()
    yield session
    # Reset mock calls to ensure clean state for the next test
    session.reset_mock()


@pytest_asyncio.fixture
async def mock_session():
    session = Mock(spec=AsyncSession)
    session.add = Mock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.get = AsyncMock()
    session.exec = AsyncMock()
    return session
