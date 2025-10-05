import asyncio
from typing import List, Optional
from app.schemas import TaskCreate, Task, TaskUpdate
from app.repositories.base_repository import BaseTaskRepository

task_list: List[Task] = []


class TaskInMemoryRepository(BaseTaskRepository):

    async def get_all_tasks(self, user_id: int) -> List[Task]:
        user_task_list = [task for task in task_list if task.user_id == user_id]
        return user_task_list

    async def get_task_by_id(self, user_id: int, task_id) -> Optional[Task]:
        return next(
            (
                task
                for task in task_list
                if task.id == task_id and task.user_id == user_id
            ),
            None,
        )

    async def create_task(self, user_id: int, task_create: TaskCreate) -> Task:
        task = Task(id=len(task_list) + 1, user_id=user_id, **task_create.model_dump())
        task_list.append(task)
        return task

    async def update_task(
        self, user_id: int, task_id: int, task_update: TaskUpdate
    ) -> Optional[Task]:
        task = await self.get_task_by_id(user_id=user_id, task_id=task_id)
        if task:
            updated_task = task_update.model_dump(exclude_unset=True)
            for key, value in updated_task.items():
                setattr(task, key, value)
            return task
        return None

    async def partial_update_task(
        self, user_id: int, task_id: int, task_update: TaskUpdate
    ) -> Optional[Task]:
        return await self.update_task(
            user_id=user_id, task_id=task_id, task_update=task_update
        )

    async def delete_task(self, user_id: int, task_id: int) -> bool:
        task = await self.get_task_by_id(user_id=user_id, task_id=task_id)
        if task:
            task_list.remove(task)
            return True
        return False
