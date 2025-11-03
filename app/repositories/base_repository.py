from abc import ABC, abstractmethod

from pydantic import EmailStr
from app.schemas import TaskCreate, Task, TaskUpdate, User, UserCreate


class BaseTaskRepository(ABC):
    @abstractmethod
    async def get_task_by_id(self, user_id: int, task_id: int) -> Task:
        pass

    @abstractmethod
    async def get_all_tasks(self, user_id: int) -> list[Task]:
        pass

    @abstractmethod
    async def create_task(self, user_id: int, task_create: TaskCreate) -> Task:
        pass

    @abstractmethod
    async def update_task(
        self, user_id: int, task_id: int, task_update: TaskUpdate
    ) -> Task:
        pass

    @abstractmethod
    async def partial_update_task(
        self,
        user_id: int,
        task_id: int,
        task_update: TaskUpdate,
    ) -> Task:
        pass

    @abstractmethod
    async def delete_task(self, user_id: int, task_id: int) -> bool:
        pass


class BaseAuthRepository(ABC):
    @abstractmethod
    async def create_user(self, user_create: UserCreate) -> User:
        pass

    @abstractmethod
    async def authenticate_user(self, username: str, password: str) -> User:
        pass

    @abstractmethod
    async def get_user_by_username(self, username: str) -> User:
        pass

    @abstractmethod
    async def get_user_by_email(self, email: EmailStr) -> User:
        pass

    @abstractmethod
    async def activate_user_account(self, username: str) -> User:
        pass
    
    @abstractmethod
    async def update_user_password(self, email: EmailStr, new_password: str) -> User:
        pass