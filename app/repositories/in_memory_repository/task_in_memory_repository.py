from typing import override
from app.schemas import TaskCreate, Task, TaskUpdate
from app.repositories.base_repository import BaseTaskRepository

task_list: list[Task] = []


class TaskInMemoryRepository(BaseTaskRepository):
    @override
    async def get_all_tasks(self, user_id: int) -> list[Task]:
        user_task_list = [task for task in task_list if task.user_id == user_id]
        return user_task_list

    @override
    async def get_task_by_id(self, user_id: int, task_id: int) -> Task:
        task = next(
            (
                task
                for task in task_list
                if task.id == task_id and task.user_id == user_id
            ),
            None,
        )
        if task is None:
            raise ValueError(f"Task {task_id} not found for user {user_id}")
        return task

    @override
    async def create_task(self, user_id: int, task_create: TaskCreate) -> Task:
        task = Task.model_validate(
            {
                **task_create.model_dump(),
                "id": len(task_list) + 1,
                "user_id": user_id,
            }
        )
        task_list.append(task)
        return task

    @override
    async def update_task(
        self, user_id: int, task_id: int, task_update: TaskUpdate
    ) -> Task:
        try:
            task = await self.get_task_by_id(user_id=user_id, task_id=task_id)
            if task:
                updated_task: dict[str, str | int] = task_update.model_dump(
                    exclude_unset=True
                )
                for key, value in updated_task.items():
                    setattr(task, key, value)
            return task
        except Exception as e:
            raise e

    @override
    async def partial_update_task(
        self, user_id: int, task_id: int, task_update: TaskUpdate
    ) -> Task:
        return await self.update_task(
            user_id=user_id, task_id=task_id, task_update=task_update
        )

    @override
    async def delete_task(self, user_id: int, task_id: int) -> bool:
        task = await self.get_task_by_id(user_id=user_id, task_id=task_id)
        if task:
            task_list.remove(task)
            return True
        return False
