from collections.abc import AsyncGenerator
from typing import cast
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.config import config


# Create async engine
engine = create_async_engine(cast(str, config.database.get("url")), echo=False)

# Create async session factory
AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker[AsyncSession](
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get a new DB session per request.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# Optional: Create tables (run once during app startup)
async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(fn=SQLModel.metadata.create_all)
