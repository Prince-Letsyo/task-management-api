import pytest
import pytest_asyncio
from unittest.mock import Mock
from sqlmodel import delete
from app.repositories import (
    TaskSQLRepository,
    TaskInMemoryRepository,
    AuthInMemoryRepository,
    AuthSQLRepository,
)
from app.schemas import TaskCreate, TaskUpdate, Task, User, UserCreate


@pytest.fixture
def in_memory_task_repository():
    return TaskInMemoryRepository()


@pytest.fixture
def in_memory_auth_repository():
    return AuthInMemoryRepository()



@pytest.mark.asyncio
async def create_user(in_memory_auth_repository, mock_user) -> User:
    mocked_user = mock_user.copy()
    user_create = UserCreate(
        username=mocked_user["username"],
        email=mocked_user["email"],
        password=mocked_user["password"],
    )
    return  await in_memory_auth_repository.create_user(user_create=user_create)


@pytest.mark.asyncio
class TestTaskInMemoryRepository:

    async def test_create_task(self, in_memory_task_repository, mock_task, create_user):
        user = await create_user
        task_data = TaskCreate(
            title=mock_task["title"],
            description=mock_task["description"],
            status=mock_task["status"],
        )
        created_task = await in_memory_task_repository.create_task(
            user_id=user.id, task_create=task_data
        )
        assert created_task.id is not None
        assert created_task.title == task_data.title
        assert created_task.description == task_data.description
        assert created_task.status == task_data.status

    async def test_get_all_tasks(
        self, in_memory_task_repository, mock_task, create_user
    ):
        user = await create_user
        task1 = TaskCreate(
            title=mock_task["title"],
            description=mock_task["description"],
            status=mock_task["status"],
        )
        task2 = TaskCreate(
            title=mock_task["title"],
            description=mock_task["description"],
            status=mock_task["status"],
        )
        await in_memory_task_repository.create_task(user_id=user.id, task_create=task1)
        await in_memory_task_repository.create_task(user_id=user.id, task_create=task2)

        tasks = await in_memory_task_repository.get_all_tasks(user_id=user.id)
        assert isinstance(tasks, list)
        assert len(tasks) >= 2  # At least the two tasks we just added

    async def test_get_task_by_id(
        self, in_memory_task_repository, mock_task, create_user
    ):
        user = await create_user
        task_data = TaskCreate(
            title=mock_task["title"],
            description=mock_task["description"],
            status=mock_task["status"],
        )
        created_task = await in_memory_task_repository.create_task(
            user_id=user.id, task_create=task_data
        )
        fetched_task = await in_memory_task_repository.get_task_by_id(
            user_id=user.id, task_id=created_task.id
        )
        assert fetched_task is not None
        assert fetched_task.id == created_task.id

    async def test_update_task(self, in_memory_task_repository, mock_task, create_user):
        user = await create_user
        task_data = TaskCreate(
            title=mock_task["title"],
            description=mock_task["description"],
            status=mock_task["status"],
        )
        created_task = await in_memory_task_repository.create_task(
            user_id=user.id, task_create=task_data
        )
        task_updated = mock_task
        update_data = TaskUpdate(
            title=task_updated["title"],
            description=task_updated["description"],
            status=task_updated["status"],
        )
        updated_task = await in_memory_task_repository.update_task(
            user_id=user.id, task_id=created_task.id, task_update=update_data
        )
        assert updated_task.title == task_updated["title"]
        assert updated_task.description == task_updated["description"]
        assert updated_task.status == task_updated["status"]

    async def test_partial_update_task(
        self, in_memory_task_repository, mock_task, create_user
    ):
        user = await create_user
        task_updated = mock_task
        task_data = TaskCreate(
            title=task_updated["title"],
            description=task_updated["description"],
            status=task_updated["status"],
        )
        created_task = await in_memory_task_repository.create_task(
            user_id=user.id, task_create=task_data
        )
        task_description_updated = mock_task["description"]
        update_data = TaskUpdate(
            description=task_description_updated,
        )
        updated_task = await in_memory_task_repository.partial_update_task(
            user_id=user.id, task_id=created_task.id, task_update=update_data
        )
        assert updated_task.title == task_updated["title"]
        assert updated_task.description == task_description_updated
        assert updated_task.status == task_updated["status"]

    async def test_delete_task(self, in_memory_task_repository, mock_task, create_user):
        user = await create_user
        task_updated = mock_task
        task_data = TaskCreate(
            title=task_updated["title"],
            description=task_updated["description"],
            status=task_updated["status"],
        )
        created_task = await in_memory_task_repository.create_task(
            user_id=user.id, task_create=task_data
        )
        result = await in_memory_task_repository.delete_task(
            user_id=user.id, task_id=created_task.id
        )
        assert result is True
        fetched_task = await in_memory_task_repository.get_task_by_id(
            user_id=user.id, task_id=created_task.id
        )
        assert fetched_task is None

    async def test_delete_task_not_found(self, in_memory_task_repository, create_user):
        user = await create_user
        result = await in_memory_task_repository.delete_task(
            user_id=user.id, task_id=9999
        )
        assert result is False


@pytest_asyncio.fixture
async def task_repository(task_mock_session):
    return TaskSQLRepository(task_mock_session)


@pytest.fixture
def auth_repository(auth_mock_session):
    return AuthSQLRepository(auth_mock_session)


@pytest.fixture
async def create_user(auth_repository, mock_user) -> User:
    mocked_user = mock_user.copy()
    user_create = UserCreate(
        username=mocked_user["username"],
        email=mocked_user["email"],
        password=mocked_user["password"],
    )
    return await auth_repository.create_user(user_create=user_create)


@pytest.mark.asyncio
class TestTaskSQLRepository:
    async def test_create_task(
        self, task_repository, task_mock_session, mock_task, create_user
    ):
        user = await create_user
        task_updated = mock_task
        task_data = TaskCreate(
            title=task_updated["title"],
            description=task_updated["description"],
            status=task_updated["status"],
        )
        mock_task_ = Task(**task_data.model_dump())
        task_mock_session.get.return_value = None
        task_mock_session.exec.return_value = Mock(all=Mock(return_value=[]))

        created_task = await task_repository.create_task(
            user_id=user.id, task_create=task_data
        )

        task_mock_session.add.assert_called_once()
        task_mock_session.commit.assert_called_once()
        task_mock_session.refresh.assert_called_once_with(
            task_mock_session.add.call_args[0][0]
        )
        assert created_task.title == task_data.title
        assert created_task.description == task_data.description
        assert created_task.status == task_data.status

    async def test_get_all_tasks(
        self, task_repository, task_mock_session, mock_task, create_user
    ):
        user = await create_user
        task = mock_task
        mock_tasked = Task(
            id=task["id"],
            title=task["title"],
            description=task["description"],
            status=task["status"],
        )
        task_mock_session.exec.return_value = Mock(all=Mock(return_value=[mock_tasked]))

        tasks = await task_repository.get_all_tasks(user_id=user.id)

        # Verify the query is a select on Task.__table__
        assert task_mock_session.exec.call_count >= 1
        query = task_mock_session.exec.call_args[0][0]
        assert str(query) == str(
            Task.__table__.select().where(Task.user_id == user.id)
        ), f"Expected query {Task.__table__.select().where(Task.user_id==user.id)}, got {query}"
        assert len(tasks) >= 1
        assert tasks[0].title == task["title"]

    async def test_get_task_by_id(
        self, task_repository, task_mock_session, mock_task, create_user
    ):
        user = await create_user
        task_ = mock_task
        mock_tasked = Task(
            id=task_["id"],
            title=task_["title"],
            description=task_["description"],
            status=task_["status"],
        )
        task_mock_session.get.return_value = mock_tasked

        task = await task_repository.get_task_by_id(
            user_id=user.id, task_id=task_["id"]
        )

        assert task.id == task_["id"]
        assert task.title == task_["title"]

    async def test_get_task_by_id_not_found(
        self, task_repository, task_mock_session, create_user
    ):
        user = await create_user
        task_mock_session.get.return_value = None

        task = await task_repository.get_task_by_id(user_id=user.id, task_id=9999)

        assert task is None

    async def test_update_task(
        self, task_repository, task_mock_session, mock_task, create_user
    ):
        user = await create_user
        task_ = mock_task
        mock_tasked = Task(
            id=task_["id"],
            title=task_["title"],
            description=task_["description"],
            status=task_["status"],
        )
        task_updated = mock_task
        task_update = TaskUpdate(
            title=task_updated["title"],
            description=task_updated["description"],
            status=task_updated["status"],
        )
        task_mock_session.get.return_value = mock_tasked

        updated_task = await task_repository.update_task(
            user_id=user.id, task_id=task_["id"], task_update=task_update
        )

        task_mock_session.add.assert_called_once_with(mock_tasked)
        task_mock_session.commit.assert_called_once()
        task_mock_session.refresh.assert_called_once_with(mock_tasked)
        assert updated_task.title == task_updated["title"]
        assert updated_task.description == task_updated["description"]
        assert updated_task.status == task_updated["status"]

    async def test_update_task_not_found(
        self, task_repository, task_mock_session, mock_task, create_user
    ):
        user = await create_user
        task_mock_session.get.return_value = None
        task_updated = mock_task
        task_update = TaskUpdate(title=task_updated["title"])

        updated_task = await task_repository.update_task(
            user_id=user.id, task_id=9999, task_update=task_update
        )

        task_mock_session.add.assert_not_called()
        task_mock_session.commit.assert_not_called()
        task_mock_session.refresh.assert_not_called()
        assert updated_task is None

    async def test_partial_update_task(
        self, task_repository, task_mock_session, mock_task, create_user
    ):
        user = await create_user
        task_ = mock_task
        mock_tasked = Task(
            id=task_["id"],
            title=task_["title"],
            description=task_["description"],
            status=task_["status"],
        )
        task_updated = mock_task
        task_update = TaskUpdate(description=task_updated["description"])
        task_mock_session.get.return_value = mock_tasked

        updated_task = await task_repository.partial_update_task(
            user_id=user.id, task_id=task_["id"], task_update=task_update
        )

        task_mock_session.add.assert_called_once_with(mock_tasked)
        task_mock_session.commit.assert_called_once()
        task_mock_session.refresh.assert_called_once_with(mock_tasked)
        assert updated_task.description == task_updated["description"]
        assert updated_task.title == task_["title"]
        assert updated_task.status == task_["status"]

    async def test_partial_update_task_not_found(
        self, task_repository, task_mock_session, create_user
    ):
        user = await create_user
        task_mock_session.get.return_value = None
        task_update = TaskUpdate(description="New description")

        updated_task = await task_repository.partial_update_task(
            user_id=user.id, task_id=9999, task_update=task_update
        )

        task_mock_session.add.assert_not_called()
        task_mock_session.commit.assert_not_called()
        task_mock_session.refresh.assert_not_called()
        assert updated_task is None

    async def test_delete_task(self, task_repository, task_mock_session, create_user):
        user = await create_user
        task_mock_session.exec.return_value = Mock(rowcount=1)

        result = await task_repository.delete_task(user_id=user.id, task_id=1)

        # Verify the query is a delete statement for Task with the correct ID
        assert task_mock_session.exec.call_count == 1
        query = task_mock_session.exec.call_args[0][0]
        expected_query = delete(Task).where(Task.id == 1 and Task.user_id == user.id)
        assert str(query) == str(
            expected_query
        ), f"Expected query {expected_query}, got {query}"
        task_mock_session.commit.assert_called_once()
        assert result is True

    async def test_delete_task_not_found(
        self, task_repository, task_mock_session, create_user
    ):
        user = await create_user
        task_mock_session.exec.return_value = Mock(rowcount=0)

        result = await task_repository.delete_task(user_id=user.id, task_id=9999)

        # Verify the query is a delete statement for Task with the correct ID
        assert task_mock_session.exec.call_count == 1
        query = task_mock_session.exec.call_args[0][0]
        expected_query = delete(Task).where(Task.id == 9999 and Task.user_id == user.id)
        assert str(query) == str(
            expected_query
        ), f"Expected query {expected_query}, got {query}"
        task_mock_session.commit.assert_called_once()
        assert result is False

    async def test_delete_task_exception(
        self, task_repository, task_mock_session, create_user
    ):
        user = await create_user
        task_mock_session.exec.side_effect = Exception("DB Error")

        result = await task_repository.delete_task(task_id=1, user_id=user.id)

        task_mock_session.commit.assert_not_called()
        assert result is False

    async def test_create_task_exception(
        self, task_repository, task_mock_session, mock_task, create_user
    ):
        user = await create_user
        task_ = mock_task
        task_data = Task(
            id=task_["id"],
            title=task_["title"],
            description=task_["description"],
            status=task_["status"],
        )
        task_mock_session.add.side_effect = Exception(
            "app.schemas.user_task_relation_schemas.TaskModel() got multiple values for keyword argument 'user_id'"
        )

        with pytest.raises(Exception) as exc_info:
            await task_repository.create_task(user_id=user.id, task_create=task_data)
        print(exc_info.value)
        assert (
            str(exc_info.value)
            == "app.schemas.user_task_relation_schemas.TaskModel() got multiple values for keyword argument 'user_id'"
        )
        task_mock_session.commit.assert_not_called()
        task_mock_session.refresh.assert_not_called()
