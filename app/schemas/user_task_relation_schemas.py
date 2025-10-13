from sqlmodel import Field, Relationship
from typing import Optional, List
from .user_schemas import UserCreate
from .task_schemas import TaskBase


class UserModel(UserCreate, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    tasks: List["TaskModel"] = Relationship(back_populates="user")


# Model for database and full task response (used in GET/POST responses)
class TaskModel(TaskBase, table=True):
    __tablename__ = "tasks"
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    # Foreign key referencing the User model
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    # Define the relationship to the User model
    user: Optional[UserModel] = Relationship(back_populates="tasks")
