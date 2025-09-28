import os
from fastapi import Depends
from dotenv import load_dotenv
from .repositories import TaskInMemoryRepository, TaskSQLRepository
from app.repositories.base_repository import BaseTaskRepository
from .services import TaskService
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db import get_db


load_dotenv()


def get_task_repository(db: AsyncSession = Depends(get_db)) -> BaseTaskRepository:
    env_mode = os.getenv("ENV_MODE", "dev")
    if env_mode == "dev":
        return TaskInMemoryRepository()
    elif env_mode == "prod":
        return TaskSQLRepository(db)
    raise ValueError(f"Unsupported ENV_MODE: {env_mode}")


def get_task_service(
    repository: BaseTaskRepository = Depends(get_task_repository),
) -> TaskService:
    return TaskService(repository)
