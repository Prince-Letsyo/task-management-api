import pytest
import pytest_asyncio
from unittest.mock import Mock
from sqlmodel import delete
from app.repositories import TaskSQLRepository, TaskInMemoryRepository
from app.schemas import TaskCreate, TaskUpdate, Task


@pytest.fixture(scope="class")
def in_memory_task_repository():
    return TaskInMemoryRepository()


@pytest.mark.asyncio
class TestTaskInMemoryRepository:
    async def test_create_task(self, in_memory_task_repository):
        task_data = TaskCreate(
            title="Test Task",
            description="Test description",
            status="pending",
        )
        created_task = await in_memory_task_repository.create_task(
            task_create=task_data
        )
        assert created_task.id is not None
        assert created_task.title == task_data.title
        assert created_task.description == task_data.description
        assert created_task.status == task_data.status

    async def test_get_all_tasks(self, in_memory_task_repository):
        task1 = TaskCreate(
            title="Task 1",
            description="Description 1",
            status="pending",
        )
        task2 = TaskCreate(
            title="Task 2",
            description="Description 2",
            status="completed",
        )
        await in_memory_task_repository.create_task(task_create=task1)
        await in_memory_task_repository.create_task(task_create=task2)

        tasks = await in_memory_task_repository.get_all_tasks()
        assert len(tasks) == 3

    async def test_get_task_by_id(self, in_memory_task_repository):
        task_data = TaskCreate(
            title="Test Task",
            description="Test description",
            status="pending",
        )
        created_task = await in_memory_task_repository.create_task(
            task_create=task_data
        )
        fetched_task = await in_memory_task_repository.get_task_by_id(
            task_id=created_task.id
        )
        assert fetched_task is not None
        assert fetched_task.id == created_task.id

    async def test_update_task(self, in_memory_task_repository):
        task_data = TaskCreate(
            title="Test Task",
            description="Test description",
            status="pending",
        )
        created_task = await in_memory_task_repository.create_task(
            task_create=task_data
        )

        update_data = TaskUpdate(
            title="Updated Title",
            description="Updated Description",
            status="completed",
        )
        updated_task = await in_memory_task_repository.update_task(
            task_id=created_task.id, task_update=update_data
        )
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Updated Description"
        assert updated_task.status == "completed"

    async def test_partial_update_task(self, in_memory_task_repository):
        task_data = TaskCreate(
            title="Test Task",
            description="Test description",
            status="pending",
        )
        created_task = await in_memory_task_repository.create_task(
            task_create=task_data
        )
        update_data = TaskUpdate(
            description="Partially Updated Description",
        )
        updated_task = await in_memory_task_repository.partial_update_task(
            task_id=created_task.id, task_update=update_data
        )
        assert updated_task.title == "Test Task"
        assert updated_task.description == "Partially Updated Description"
        assert updated_task.status == "pending"

    async def test_delete_task(self, in_memory_task_repository):
        task_data = TaskCreate(
            title="Test Task",
            description="Test description",
            status="pending",
        )
        created_task = await in_memory_task_repository.create_task(
            task_create=task_data
        )
        result = await in_memory_task_repository.delete_task(task_id=created_task.id)
        assert result is True
        fetched_task = await in_memory_task_repository.get_task_by_id(
            task_id=created_task.id
        )
        assert fetched_task is None
    async def test_delete_task_not_found(self, in_memory_task_repository):
        result = await in_memory_task_repository.delete_task(task_id=9999)
        assert result is False

@pytest_asyncio.fixture
async def task_repository(mock_session):
    return TaskSQLRepository(mock_session)


@pytest.mark.asyncio
class TestTaskSQLRepository:
    async def test_create_task(self, task_repository, mock_session):
        task_data = TaskCreate(
            title="Test Task",
            description="Test description",
            status="pending",
        )
        mock_task = Task(**task_data.model_dump())
        mock_session.get.return_value = None
        mock_session.exec.return_value = Mock(all=Mock(return_value=[]))

        created_task = await task_repository.create_task(task_create=task_data)

        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(mock_session.add.call_args[0][0])
        assert created_task.title == task_data.title
        assert created_task.description == task_data.description
        assert created_task.status == task_data.status

    async def test_get_all_tasks(self, task_repository, mock_session):
        mock_task = Task(
            id=1, title="Test Task", description="Test description", status="pending"
        )
        mock_session.exec.return_value = Mock(all=Mock(return_value=[mock_task]))

        tasks = await task_repository.get_all_tasks()

        # Verify the query is a select on Task.__table__
        assert mock_session.exec.call_count == 1
        query = mock_session.exec.call_args[0][0]
        assert str(query) == str(
            Task.__table__.select()
        ), f"Expected query {Task.__table__.select()}, got {query}"
        assert len(tasks) == 1
        assert tasks[0].title == "Test Task"

    async def test_get_task_by_id(self, task_repository, mock_session):
        mock_task = Task(
            id=1, title="Test Task", description="Test description", status="pending"
        )
        mock_session.get.return_value = mock_task

        task = await task_repository.get_task_by_id(task_id=1)

        mock_session.get.assert_called_once_with(Task, 1)
        assert task.id == 1
        assert task.title == "Test Task"

    async def test_get_task_by_id_not_found(self, task_repository, mock_session):
        mock_session.get.return_value = None

        task = await task_repository.get_task_by_id(task_id=9999)

        mock_session.get.assert_called_once_with(Task, 9999)
        assert task is None

    async def test_update_task(self, task_repository, mock_session):
        mock_task = Task(
            id=1, title="Old Title", description="Old description", status="pending"
        )
        task_update = TaskUpdate(
            title="New Title", description="New description", status="completed"
        )
        mock_session.get.return_value = mock_task

        updated_task = await task_repository.update_task(
            task_id=1, task_update=task_update
        )

        mock_session.get.assert_called_once_with(Task, 1)
        mock_session.add.assert_called_once_with(mock_task)
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(mock_task)
        assert updated_task.title == "New Title"
        assert updated_task.description == "New description"
        assert updated_task.status == "completed"

    async def test_update_task_not_found(self, task_repository, mock_session):
        mock_session.get.return_value = None
        task_update = TaskUpdate(title="New Title")

        updated_task = await task_repository.update_task(
            task_id=9999, task_update=task_update
        )

        mock_session.get.assert_called_once_with(Task, 9999)
        mock_session.add.assert_not_called()
        mock_session.commit.assert_not_called()
        mock_session.refresh.assert_not_called()
        assert updated_task is None

    async def test_partial_update_task(self, task_repository, mock_session):
        mock_task = Task(
            id=1, title="Old Title", description="Old description", status="pending"
        )
        task_update = TaskUpdate(description="New description")
        mock_session.get.return_value = mock_task

        updated_task = await task_repository.partial_update_task(
            task_id=1, task_update=task_update
        )

        mock_session.get.assert_called_once_with(Task, 1)
        mock_session.add.assert_called_once_with(mock_task)
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(mock_task)
        assert updated_task.description == "New description"
        assert updated_task.title == "Old Title"
        assert updated_task.status == "pending"

    async def test_partial_update_task_not_found(self, task_repository, mock_session):
        mock_session.get.return_value = None
        task_update = TaskUpdate(description="New description")

        updated_task = await task_repository.partial_update_task(
            task_id=9999, task_update=task_update
        )

        mock_session.get.assert_called_once_with(Task, 9999)
        mock_session.add.assert_not_called()
        mock_session.commit.assert_not_called()
        mock_session.refresh.assert_not_called()
        assert updated_task is None

    async def test_delete_task(self, task_repository, mock_session):
        mock_session.exec.return_value = Mock(rowcount=1)

        result = await task_repository.delete_task(task_id=1)

        # Verify the query is a delete statement for Task with the correct ID
        assert mock_session.exec.call_count == 1
        query = mock_session.exec.call_args[0][0]
        expected_query = delete(Task).where(Task.id == 1)
        assert str(query) == str(
            expected_query
        ), f"Expected query {expected_query}, got {query}"
        mock_session.commit.assert_called_once()
        assert result is True

    async def test_delete_task_not_found(self, task_repository, mock_session):
        mock_session.exec.return_value = Mock(rowcount=0)

        result = await task_repository.delete_task(task_id=9999)

        # Verify the query is a delete statement for Task with the correct ID
        assert mock_session.exec.call_count == 1
        query = mock_session.exec.call_args[0][0]
        expected_query = delete(Task).where(Task.id == 9999)
        assert str(query) == str(
            expected_query
        ), f"Expected query {expected_query}, got {query}"
        mock_session.commit.assert_called_once()
        assert result is False

    async def test_delete_task_exception(self, task_repository, mock_session):
        mock_session.exec.side_effect = Exception("DB Error")

        result = await task_repository.delete_task(task_id=1)

        mock_session.commit.assert_not_called()
        assert result is False

    async def test_create_task_exception(self, task_repository, mock_session):
        task_data = TaskCreate(
            title="Test Task",
            description="Test description",
            status="pending",
        )
        mock_session.add.side_effect = Exception("DB Error")

        with pytest.raises(Exception) as exc_info:
            await task_repository.create_task(task_create=task_data)

        assert str(exc_info.value) == "DB Error"
        mock_session.commit.assert_not_called()
        mock_session.refresh.assert_not_called()
