from typing import cast, override
from app.schemas import TaskCreate, Task, TaskUpdate
from app.repositories.base_repository import BaseTaskRepository

tasks: dict[int, Task] = {}


class TaskInMemoryRepository(BaseTaskRepository):
    @override
    async def get_all_tasks(self, user_id: int) -> list[Task]:
        task_list: list[Task] = [
            task for task in tasks.values() if task.user_id == user_id
        ]
        return task_list

    @override
    async def get_task_by_id(self, user_id: int, task_id: int) -> Task:
        task: Task | None = next(
            (
                task
                for task in tasks.values()
                if task.id == task_id and task.user_id == user_id
            ),
            None,
        )
        if task:
            return task
        raise Exception("Task not found")

    @override
    async def create_task(self, user_id: int, task_create: TaskCreate) -> Task:
        task: Task = Task.model_validate(
            {
                **task_create.model_dump(),
                "id": len(tasks) + 1,
                "user_id": user_id,
            }
        )
        tasks[cast(int, task.id)] = task
        return task

    @override
    async def update_task(
        self, user_id: int, task_id: int, task_update: TaskUpdate
    ) -> Task:
        task: Task = await self.get_task_by_id(user_id=user_id, task_id=task_id)
        updated_task: Task = task.model_copy(update=task_update.model_dump())
        tasks[cast(int, task.id)] = updated_task
        return updated_task

    @override
    async def partial_update_task(
        self, user_id: int, task_id: int, task_update: TaskUpdate
    ) -> Task:
        return await self.update_task(
            user_id=user_id, task_id=task_id, task_update=task_update
        )

    @override
    async def delete_task(self, user_id: int, task_id: int) -> bool:
        task: Task = await self.get_task_by_id(user_id=user_id, task_id=task_id)
        del tasks[cast(int, task.id)]
        return True
