from abc import ABC, abstractmethod
from typing import List, Optional
from app.schemas import TaskCreate, Task, TaskUpdate


class BaseTaskRepository(ABC):
    @abstractmethod
    async def get_task_by_id(self, task_id: int) -> Optional[Task]:
        pass

    @abstractmethod
    async def get_all_tasks(self) -> List[Task]:
        pass

    @abstractmethod
    async def create_task(self, task_create: TaskCreate) -> Task:
        pass

    @abstractmethod
    async def update_task(
        self, task_id: int, task_update: TaskUpdate, exclude_unset: bool = False
    ) -> Optional[Task]:
        pass

    @abstractmethod
    async def partial_update_task(
        self, task_id: int, task_update: TaskUpdate, exclude_unset: bool = True
    ) -> Optional[Task]:
        pass

    @abstractmethod
    async def delete_task(self, task_id: int) -> bool:
        pass
