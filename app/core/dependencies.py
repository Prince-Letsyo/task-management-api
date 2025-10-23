from typing import ClassVar, Self
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from .db import get_db_session
from app.repositories import TaskSQLRepository, AuthSQLRepository
from app.repositories.base_repository import BaseTaskRepository, BaseAuthRepository
from app.services import TaskService, AuthService


class DependencyContainer:
    _instance: ClassVar["DependencyContainer | None"] = None
    task_repository: BaseTaskRepository | None = None
    auth_repository: BaseAuthRepository | None = None
    task_service: TaskService | None = None
    auth_service: AuthService | None = None

    def __new__(cls) -> Self | "DependencyContainer":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def initialize(self, db: AsyncSession) -> None:
        if self.task_repository is None or self.auth_repository is None:
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
dependency_container: DependencyContainer = DependencyContainer()


async def get_task_service(
    session: AsyncSession = Depends(
        dependency=get_db_session
    ),  # pyright: ignore[reportCallInDefaultInitializer]
) -> TaskService:
    await dependency_container.initialize(session)
    if dependency_container.task_service is None:
        raise ValueError(
            "TaskService not initialized. Ensure repositories are set up first."
        )
    service = dependency_container.task_service
    await dependency_container.cleanup()
    return service


async def get_auth_service(
    session: AsyncSession = Depends(
        dependency=get_db_session
    ),  # pyright: ignore[reportCallInDefaultInitializer]
) -> AuthService:
    await dependency_container.initialize(db=session)
    if dependency_container.auth_service is None:
        raise ValueError(
            "AuthService not initialized. Ensure repositories are set up first."
        )
    service = dependency_container.auth_service
    await dependency_container.cleanup()
    return service
