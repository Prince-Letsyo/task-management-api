from typing import List, Optional
from app.schemas import TaskCreate, Task, TaskUpdate
from app.repositories.base_repository import BaseTaskRepository


class TaskInMemoryRepository(BaseTaskRepository):
    def __init__(self):
        self.tasks: List[Task] = []
        self.current_id = 1

    async def get_all_tasks(self) -> List[Task]:
        return self.tasks

    async def get_task_by_id(self, task_id) -> Optional[Task]:
        return next((task for task in self.tasks if task.id == task_id), None)

    async def create_task(self, task_create: TaskCreate) -> Task:
        task = Task(id=self.current_id, **task_create.model_dump())
        self.tasks.append(task)
        self.current_id += 1
        return task

    async def update_task(
        self, task_id: int, task_update: TaskUpdate, exclude_unset: bool = False
    ) -> Optional[Task]:
        task = await self.get_task_by_id(task_id)
        if task:
            updated_task = task_update.model_dump(exclude_unset=exclude_unset)
            for key, value in updated_task.items():
                setattr(task, key, value)
            return task
        return None

    async def partial_update_task(
        self, task_id: int, task_update: TaskUpdate, exclude_unset: bool = True
    ) -> Optional[Task]:
        return self.update_task(task_id, task_update, exclude_unset=exclude_unset)

    async def delete_task(self, task_id: int) -> bool:
        task = await self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False
