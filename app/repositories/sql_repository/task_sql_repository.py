from typing import override
from app.schemas import TaskCreate, Task, TaskUpdate
from app.repositories.base_repository import BaseTaskRepository
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.engine import ScalarResult
from sqlmodel import select


class TaskSQLRepository(BaseTaskRepository):
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    @override
    async def get_all_tasks(self, user_id: int) -> list[Task]:
        try:
            result: ScalarResult[Task] = await self.db.exec(
                select(Task).where(Task.user_id == user_id)
            )
            return list(result.all())
        except Exception as e:
            raise e

    @override
    async def get_task_by_id(self, user_id: int, task_id: int) -> Task:
        try:
            result: ScalarResult[Task] = await self.db.exec(
                select(Task).where(Task.id == task_id and Task.user_id == user_id)
            )
            return result.one()
        except Exception as e:
            raise e

    @override
    async def create_task(self, user_id: int, task_create: TaskCreate) -> Task:
        try:
            new_task = Task.model_validate(
                {**task_create.model_dump(), "user_id": user_id}
            )
            self.db.add(new_task)
            await self.db.commit()
            await self.db.refresh(new_task)
            return new_task
        except Exception as e:
            raise e

    @override
    async def update_task(
        self,
        user_id: int,
        task_id: int,
        task_update: TaskUpdate,
    ) -> Task:
        try:

            task = await self.get_task_by_id(user_id=user_id, task_id=task_id)
            task_data: dict[str, str | int] = task_update.model_dump(exclude_unset=True)
            for key, value in task_data.items():
                setattr(task, key, value)
            self.db.add(task)
            await self.db.commit()
            await self.db.refresh(task)
            return task
        except Exception as e:
            raise e

    @override
    async def partial_update_task(
        self, user_id: int, task_id: int, task_update: TaskUpdate
    ) -> Task:
        try:
            return await self.update_task(
                user_id=user_id, task_id=task_id, task_update=task_update
            )
        except Exception as e:
            raise e

    @override
    async def delete_task(self, user_id: int, task_id: int) -> bool:
        try:
            task = await self.get_task_by_id(user_id=user_id, task_id=task_id)
            await self.db.delete(task)
            await self.db.commit()
            return True
        except Exception as e:
            raise e
