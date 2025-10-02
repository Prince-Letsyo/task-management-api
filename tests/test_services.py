import pytest
import pytest_asyncio
from app.services.task_service import TaskService
from app.repositories import TaskSQLRepository
from app.schemas import TaskCreate, TaskUpdate

@pytest_asyncio.fixture
async def task_service(session):
    return TaskService(repository=TaskSQLRepository(session))

@pytest.mark.asyncio
class TestTaskServiceAsync:
    async def test_create_task(self, task_service):
        task_data = TaskCreate(
            title="Async Service Test Task",
            description="This is a test task for async service",
            status="pending",
        )
        new_task = await task_service.create_task(task_create=task_data)
        assert new_task.title == task_data.title
        assert new_task.description == task_data.description
        assert new_task.status == task_data.status
        assert new_task.id is not None

    async def test_get_all_tasks(self, task_service):
        tasks = await task_service.get_all_tasks()
        assert isinstance(tasks, list)

    async def test_get_task_by_id(self, task_service):
        task = await task_service.get_task_by_id(task_id=1)
        assert task is None or task.id == 1

    async def test_update_task(self, task_service):
        # Create a task first to ensure it exists
        task_data = TaskCreate(
            title="Initial Task",
            description="Initial description",
            status="pending",
        )
        created_task = await task_service.create_task(task_create=task_data)
        
        task_update_data = TaskUpdate(
            title="Updated Async Service Test Task",
            description="This is an updated async test task for service",
            status="completed",
        )
        updated_task = await task_service.update_task(
            task_id=created_task.id, task_update=task_update_data
        )
        assert updated_task.title == task_update_data.title
        assert updated_task.description == task_update_data.description
        assert updated_task.status == task_update_data.status

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
        new_task = await task_service.create_task(task_create=task_data)
        fetched_task = await task_service.get_task_by_id(task_id=new_task.id)
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