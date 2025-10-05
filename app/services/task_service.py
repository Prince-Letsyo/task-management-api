from fastapi import HTTPException, status
from typing import List, Optional

from app.schemas import TaskCreate, Task, TaskUpdate
from app.repositories.base_repository import BaseTaskRepository, BaseAuthRepository


class TaskService:
    def __init__(
        self, task_repository: BaseTaskRepository, auth_repository: BaseAuthRepository
    ):
        self.task_repository = task_repository
        self.auth_repository = auth_repository

    async def get_all_tasks(self, username: str) -> List[Task]:
        user = await self.auth_repository.get_user_by_username(username=username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized operation",
            )
        return await self.task_repository.get_all_tasks(user_id=user.id)

    async def get_task_by_id(self, username: str, task_id: int) -> Optional[Task]:
        user = await self.auth_repository.get_user_by_username(username=username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized operation",
            )
        return await self.task_repository.get_task_by_id(
            user_id=user.id, task_id=task_id
        )

    async def create_task(self, username: str, task_create: TaskCreate) -> Task:
        user = await self.auth_repository.get_user_by_username(username=username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized operation",
            )
        return await self.task_repository.create_task(
            user_id=user.id, task_create=task_create
        )

    async def update_task(
        self, username: str, task_id: int, task_update: TaskUpdate
    ) -> Optional[Task]:
        user = await self.auth_repository.get_user_by_username(username=username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized operation",
            )
        return await self.task_repository.update_task(
            user_id=user.id, task_id=task_id, task_update=task_update
        )

    async def partial_update_task(
        self, username: str, task_id: int, task_update: TaskUpdate
    ) -> Optional[Task]:
        user = await self.auth_repository.get_user_by_username(username=username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized operation",
            )
        return await self.task_repository.partial_update_task(
            user_id=user.id, task_id=task_id, task_update=task_update
        )

    async def delete_task(self, username: str, task_id: int) -> bool:
        user = await self.auth_repository.get_user_by_username(username=username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized operation",
            )
        return await self.task_repository.delete_task(user_id=user.id, task_id=task_id)
