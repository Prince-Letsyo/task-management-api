from typing import List, Optional
from app.schemas import TaskCreate, Task, TaskUpdate
from app.repositories.base_repository import BaseTaskRepository
from app.db import TaskModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, insert


class TaskSQLRepository(BaseTaskRepository):
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_all_tasks(self) -> List[Task]:
        result = await self.db.execute(select(TaskModel))
        tasks = result.scalars().all()
        return [Task.model_validate(task) for task in tasks]

    async def get_task_by_id(self, task_id: int) -> Optional[Task]:
        result = await self.db.execute(select(TaskModel).where(TaskModel.id == task_id))
        task = result.scalar_one_or_none()
        return Task.model_validate(task) if task else None

    async def create_task(self, task_create: TaskCreate) -> Task:
        new_task = await self.db.execute(
            insert(TaskModel).values(**task_create.model_dump()).returning(TaskModel)
        )
        created_task = new_task.scalar_one()
        await self.db.commit()
        return Task.model_validate(created_task)

    async def update_task(
        self,
        task_id: int,
        task_update: TaskUpdate,
    ) -> Optional[Task]:
        result = await self.db.execute(
            update(TaskModel)
            .where(TaskModel.id == task_id)
            .values(**task_update.model_dump(exclude_unset=True))
            .returning(TaskModel)
        )
        updated_task = result.scalar_one_or_none()
        if updated_task:
            await self.db.commit()
            return Task.model_validate(updated_task)
        return None

    async def partial_update_task(
        self, task_id: int, task_update: TaskUpdate
    ) -> Optional[Task]:
        return await self.update_task(task_id, task_update)

    async def delete_task(self, task_id: int) -> bool:
        result = await self.db.execute(delete(TaskModel).where(TaskModel.id == task_id))
        await self.db.commit()
        return result.rowcount > 0
