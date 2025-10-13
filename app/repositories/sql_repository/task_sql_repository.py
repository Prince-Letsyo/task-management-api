from typing import List, Optional
from app.schemas import TaskCreate, Task, TaskUpdate
from app.repositories.base_repository import BaseTaskRepository
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import (
    IntegrityError,
    OperationalError,
    DataError,
    ProgrammingError,
    SQLAlchemyError,
)
from sqlmodel import delete


class TaskSQLRepository(BaseTaskRepository):
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_all_tasks(self, user_id: int) -> List[Task]:
        try:
            result = await self.db.exec(
                Task.__table__.select().where(Task.user_id == user_id)
            )
            return result.all()
        except Exception as e:
            raise e

    async def get_task_by_id(self, user_id: int, task_id: int) -> Optional[Task]:
        return await self.db.get(Task, task_id=task_id, user_id=user_id)

    async def create_task(self, user_id: int, task_create: TaskCreate) -> Task:
        new_task = Task(user_id=user_id, **task_create.model_dump())
        self.db.add(new_task)
        await self.db.commit()
        await self.db.refresh(new_task)
        return new_task

    async def update_task(
        self,
        user_id: int,
        task_id: int,
        task_update: TaskUpdate,
    ) -> Optional[Task]:
        task = await self.get_task_by_id(user_id=user_id, task_id=task_id)
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
        self, user_id: int, task_id: int, task_update: TaskUpdate
    ) -> Optional[Task]:
        return await self.update_task(
            user_id=user_id, task_id=task_id, task_update=task_update
        )

    async def delete_task(self, user_id: int, task_id: int) -> bool:
        try:
            result = await self.db.exec(
                delete(Task).where(Task.id == task_id and Task.user_id == user_id)
            )
            await self.db.commit()
            if result.rowcount > 0:
                return True
            return False
        except Exception:
            return False
