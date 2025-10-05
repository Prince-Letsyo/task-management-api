from sqlmodel import Field, Relationship
from typing import Optional, List
from .user_schemas import UserBase
from .task_schemas import TaskBase


class UserModel(UserBase, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    password: str = Field(nullable=False)
    # Define the relationship to the Task model (one-to-many)
    tasks: List["TaskModel"] = Relationship(back_populates="user")


# Model for database and full task response (used in GET/POST responses)
class TaskModel(TaskBase, table=True ):
    __tablename__ = "tasks"
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    # Foreign key referencing the User model
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    # Define the relationship to the User model
    user: Optional[UserModel] = Relationship(back_populates="tasks")
