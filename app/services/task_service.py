from typing import cast
from app.schemas import TaskCreate, Task, TaskUpdate
from app.repositories.base_repository import BaseTaskRepository, BaseAuthRepository


class TaskService:
    def __init__(
        self, task_repository: BaseTaskRepository, auth_repository: BaseAuthRepository
    ):
        self.task_repository: BaseTaskRepository = task_repository
        self.auth_repository: BaseAuthRepository = auth_repository

    async def get_all_tasks(self, username: str) -> list[Task]:
        try:
            user = await self.auth_repository.get_user_by_username(username=username)
            return await self.task_repository.get_all_tasks(user_id=cast(int, user.id))
        except Exception as e:
            raise e

    async def get_task_by_id(self, username: str, task_id: int) -> Task:
        try:
            user = await self.auth_repository.get_user_by_username(username=username)
            return await self.task_repository.get_task_by_id(
                user_id=cast(int, user.id), task_id=task_id
            )
        except Exception as e:
            raise e

    async def create_task(self, username: str, task_create: TaskCreate) -> Task:
        try:
            user = await self.auth_repository.get_user_by_username(username=username)
            return await self.task_repository.create_task(
                user_id=cast(int, user.id), task_create=task_create
            )
        except Exception as e:
            raise e

    async def update_task(
        self, username: str, task_id: int, task_update: TaskUpdate
    ) -> Task:
        try:
            user = await self.auth_repository.get_user_by_username(username=username)
            return await self.task_repository.update_task(
                user_id=cast(int, user.id), task_id=task_id, task_update=task_update
            )
        except Exception as e:
            raise e

    async def partial_update_task(
        self, username: str, task_id: int, task_update: TaskUpdate
    ) -> Task:
        try:
            user = await self.auth_repository.get_user_by_username(username=username)
            return await self.task_repository.partial_update_task(
                user_id=cast(int, user.id), task_id=task_id, task_update=task_update
            )
        except Exception as e:
            raise e

    async def delete_task(self, username: str, task_id: int) -> bool:
        try:
            user = await self.auth_repository.get_user_by_username(username=username)
            return await self.task_repository.delete_task(
                user_id=cast(int, user.id), task_id=task_id
            )
        except Exception as e:
            raise e
