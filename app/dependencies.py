from fastapi import Depends
from .repositories import (
    TaskInMemoryRepository,
    TaskSQLRepository,
    AuthSQLRepository,
    AuthInMemoryRepository,
)
from app.repositories.base_repository import BaseTaskRepository, BaseAuthRepository
from .services import TaskService, AuthService
from sqlmodel.ext.asyncio.session import AsyncSession
from app.config.db import get_db
from app.utils import ENV_MODE


def get_task_repository(db: AsyncSession = Depends(get_db)) -> BaseTaskRepository:
    if ENV_MODE == "dev":
        return TaskInMemoryRepository()
    elif ENV_MODE == "prod":
        return TaskSQLRepository(db)
    raise ValueError(f"Unsupported ENV_MODE: {ENV_MODE}")


def get_auth_repository(db: AsyncSession = Depends(get_db)) -> BaseAuthRepository:
    if ENV_MODE == "dev":
        return AuthInMemoryRepository()
    elif ENV_MODE == "prod":
        return AuthSQLRepository(db)
    raise ValueError(f"Unsupported ENV_MODE: {ENV_MODE}")


def get_task_service(
    repository: BaseTaskRepository = Depends(get_task_repository),
) -> TaskService:
    return TaskService(repository)


def get_auth_service(
    repository: BaseAuthRepository = Depends(get_auth_repository),
) -> AuthService:
    return AuthService(repository)
