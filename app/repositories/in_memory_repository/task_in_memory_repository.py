import asyncio
from typing import List, Optional
from app.schemas import TaskCreate, Task, TaskUpdate
from app.repositories.base_repository import BaseTaskRepository

task_list: List[Task] = []
task_list_lock = asyncio.Lock()

class TaskInMemoryRepository(BaseTaskRepository):

    async def get_all_tasks(self) -> List[Task]:
        async with task_list_lock:
            return list(task_list)

    async def get_task_by_id(self, task_id) -> Optional[Task]:
        async with task_list_lock:
            return next((task for task in task_list if task.id == task_id), None)

    async def create_task(self, task_create: TaskCreate) -> Task:
        async with task_list_lock:
            task = Task(id=len(task_list) + 1, **task_create.model_dump())
            task_list.append(task)
            return task

    async def update_task(
        self, task_id: int, task_update: TaskUpdate
    ) -> Optional[Task]:
        async with task_list_lock:
            task = next((task for task in task_list if task.id == task_id), None)
            if task:
                updated_task = task_update.model_dump(exclude_unset=True)
                for key, value in updated_task.items():
                    setattr(task, key, value)
                return task
            return None

    async def partial_update_task(
        self, task_id: int, task_update: TaskUpdate
    ) -> Optional[Task]:
        return await self.update_task(task_id, task_update)

    async def delete_task(self, task_id: int) -> bool:
        async with task_list_lock:
            task = next((task for task in task_list if task.id == task_id), None)
            if task:
                task_list.remove(task)
                return True
            return False
