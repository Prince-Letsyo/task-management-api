from faker import Faker
import pytest
from app.schemas import UserCreate
from app.repositories import AuthInMemoryRepository
from tests.conftest import UserTyped


@pytest.fixture
def in_memory_auth_repository():
    return AuthInMemoryRepository()


@pytest.mark.asyncio
class TestAuthInMemoryRepository:
    async def test_create_user(
        self, in_memory_auth_repository: AuthInMemoryRepository, mock_user: UserTyped
    ):
        mocked_user = mock_user.copy()
        user_create = UserCreate.model_validate({**mocked_user})
        user = await in_memory_auth_repository.create_user(user_create)
        assert user.username == mocked_user["username"]
        assert user.email == mocked_user["email"]
        assert user.password != mocked_user["password"]
        assert user.id is not None
        assert user.password is not None

    async def test_authenticate_user(
        self, in_memory_auth_repository: AuthInMemoryRepository, mock_user: UserTyped
    ):
        mocked_user = mock_user.copy()
        user_create = UserCreate.model_validate({**mocked_user})

        _ = await in_memory_auth_repository.create_user(user_create)
        user = await in_memory_auth_repository.authenticate_user(
            user_create.username, mocked_user["password"]
        )
        assert user.username == mocked_user["username"]
        assert user.email == mocked_user["email"]
        assert user.id is not None
