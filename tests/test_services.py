import pytest
import os
from dotenv import load_dotenv
import pytest
from app.services.task_service import TaskService
from app.db.db import get_db
from app.repositories import TaskInMemoryRepository, TaskSQLRepository
from app.schemas import TaskCreate, Task, TaskUpdate
load_dotenv()


@pytest.fixture(scope="class")
def task_service():
    # # Instantiate the actual TaskService with a real or mock repository
    env_mode = os.getenv("ENV_MODE", "dev")
    if env_mode == "dev":
        return TaskService(repository=TaskInMemoryRepository())
    elif env_mode == "prod":
        return TaskService(repository=TaskSQLRepository(get_db))
    raise ValueError(f"Unsupported ENV_MODE: {env_mode}")


@pytest.mark.asyncio
class TestTaskServiceAsync:
    async def test_create_task(self, task_service):
        task_data = TaskCreate(
            title="Async Service Test Task",
            description="This is a test task for async service",
            due_date="2024-12-31",
        )
        new_task = await task_service.create_task(task_create=task_data)
        assert new_task.title == task_data.title
        assert new_task.description == task_data.description
        assert new_task.due_date == task_data.due_date

    async def test_get_all_tasks(self, task_service):
        tasks = await task_service.get_all_tasks()
        assert isinstance(tasks, list)

    async def test_get_task_by_id(self, task_service):
        task = await task_service.get_task_by_id(task_id=1)
        assert task is None or task.id == 1

    async def test_update_task(self, task_service):
        task_update_data = TaskUpdate(
            title="Updated Async Service Test Task",
            description="This is an updated async test task for service",
            due_date="2025-01-31",
        )
        updated_task = await task_service.update_task(
            task_id=1, task_update=task_update_data
        )
        assert updated_task is None or updated_task.title == task_update_data.title
        assert (
            updated_task is None
            or updated_task.description == task_update_data.description
        )
        assert (
            updated_task is None
            or updated_task.due_date == task_update_data.due_date
        )

    async def test_partial_update_task(self, task_service):
        partial_update_data = TaskUpdate(
            description="This is a partially updated async test task for service"
        )
        partial_updated_task = await task_service.partial_update_task(
            task_id=1, task_update=partial_update_data
        )
        assert (
            partial_updated_task is None
            or partial_updated_task.description == partial_update_data.description
        )

    async def test_delete_task(self, task_service):
        result = await task_service.delete_task(task_id=1)
        assert isinstance(result, bool)
        task = await task_service.get_task_by_id(task_id=1)
        assert task is None

    async def test_create_and_get_task(self, task_service):
        task_data = TaskCreate(
            title="Route-based Service Test",
            description="Testing create and get by id",
            due_date="2024-11-30",
        )
        print(f"Task length before creation: {len(await task_service.get_all_tasks())}")
        new_task = await task_service.create_task(task_create=task_data)
        print(f"Created task: {new_task}")
        print(f"Task length after creation: {len(await task_service.get_all_tasks())}")
        fetched_task = await task_service.get_task_by_id(task_id=new_task.id)
        print(f"Fetched task: {fetched_task}")
        assert fetched_task is not None
        assert fetched_task.title == task_data.title

    async def test_update_nonexistent_task(self, task_service):
        update_data = TaskUpdate(
            title="Nonexistent",
            description="Should not update",
            due_date="2025-01-01",
        )
        updated_task = await task_service.update_task(
            task_id=9999, task_update=update_data
        )
        assert updated_task is None

    async def test_partial_update_nonexistent_task(self, task_service):
        partial_update_data = TaskUpdate(description="Should not update")
        partial_updated_task = await task_service.partial_update_task(
            task_id=9999, task_update=partial_update_data
        )
        assert partial_updated_task is None

    async def test_delete_nonexistent_task(self, task_service):
        result = await task_service.delete_task(task_id=9999)
        assert result is False
