from typing import List, Optional
from app.schemas import TaskCreate, Task, TaskUpdate
from app.repositories.base_repository import BaseTaskRepository


class TaskService:
    def __init__(self, repository: BaseTaskRepository):
        self.repository = repository

    async def get_all_tasks(self) -> List[Task]:
        return await self.repository.get_all_tasks()

    async def get_task_by_id(self, task_id: int) -> Optional[Task]:
        return await self.repository.get_task_by_id(task_id)

    async def create_task(self, task_create: TaskCreate) -> Task:
        return await self.repository.create_task(task_create)

    async def update_task(
        self, task_id: int, task_update: TaskUpdate
    ) -> Optional[Task]:
        return await self.repository.update_task(task_id, task_update)

    async def partial_update_task(
        self, task_id: int, task_update: TaskUpdate
    ) -> Optional[Task]:
        return await self.repository.partial_update_task(task_id, task_update)

    async def delete_task(self, task_id: int) -> bool:
        return await self.repository.delete_task(task_id)