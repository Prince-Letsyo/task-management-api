from sqlmodel.ext.asyncio.session import AsyncSession
from app.repositories import (
    TaskSQLRepository,
    AuthSQLRepository,
)
from app.repositories.base_repository import BaseTaskRepository, BaseAuthRepository
from app.services import TaskService, AuthService

# from app.db import get_db
from typing import Optional


class DependencyContainer:
    _instance = None
    task_repository: Optional[BaseTaskRepository] = None
    auth_repository: Optional[BaseAuthRepository] = None
    task_service: Optional[TaskService] = None
    auth_service: Optional[AuthService] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def initialize(self, db: Optional[AsyncSession] = None):
        if self.task_repository is None or self.auth_repository is None:
            # Initialize repositories based on environment
            if db is None:
                raise ValueError("Database session required for SQL repositories")
            self.task_repository = TaskSQLRepository(db)
            self.auth_repository = AuthSQLRepository(db)

            # Initialize services with singleton repositories
            self.task_service = TaskService(
                auth_repository=self.auth_repository,
                task_repository=self.task_repository,
            )
            self.auth_service = AuthService(repository=self.auth_repository)

    async def cleanup(self):
        self.task_repository = None
        self.auth_repository = None
        self.task_service = None
        self.auth_service = None


# Global container instance
dependency_container = DependencyContainer()


def get_task_service() -> TaskService:
    if dependency_container.task_service is None:
        raise ValueError(
            "TaskService not initialized. Ensure repositories are set up first."
        )
    return dependency_container.task_service


def get_auth_service() -> AuthService:
    if dependency_container.auth_service is None:
        raise ValueError(
            "AuthService not initialized. Ensure repositories are set up first."
        )
    return dependency_container.auth_service
