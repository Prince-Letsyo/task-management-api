from typing import List, Optional
from app.schemas import TaskCreate, Task, TaskUpdate
from app.repositories.base_repository import BaseTaskRepository
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import delete


class TaskSQLRepository(BaseTaskRepository):
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_all_tasks(self) -> List[Task]:
        result = await self.db.exec(Task.__table__.select())
        return result.all()

    async def get_task_by_id(self, task_id: int) -> Optional[Task]:
        return await self.db.get(Task, task_id)

    async def create_task(self, task_create: TaskCreate) -> Task:
        new_task = Task(**task_create.model_dump())
        self.db.add(new_task)
        await self.db.commit()
        await self.db.refresh(new_task)
        return new_task

    async def update_task(
        self,
        task_id: int,
        task_update: TaskUpdate,
    ) -> Optional[Task]:
        task = await self.get_task_by_id(task_id)
        if not task:
            return None
        task_data = task_update.model_dump(exclude_unset=True)
        for key, value in task_data.items():
            setattr(task, key, value)
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def partial_update_task(
        self, task_id: int, task_update: TaskUpdate
    ) -> Optional[Task]:
        return await self.update_task(task_id, task_update)

    async def delete_task(self, task_id: int) -> bool:
        try:
            result = await self.db.exec(delete(Task).where(Task.id == task_id))
            await self.db.commit()
            if result.rowcount > 0:
                return True
            return False
        except Exception:
            return False
