from typing import cast
from sqlmodel import Field, Relationship
from .user_schemas import UserBase
from .task_schemas import TaskBase


class UserModel(UserBase, table=True):
    __tablename__ = "users"  # pyright: ignore[reportUnannotatedClassAttribute, reportAssignmentType]
    id: int | None = Field(default=None, primary_key=True, index=True)
    hashed_password: str = Field(nullable=False, max_length=256)
    is_active:bool=Field(default=False, nullable=False)
    tasks: list["TaskModel"] = cast(
        list["TaskModel"], Relationship(back_populates="user")
    )


# Model for database and full task response (used in GET/POST responses)
class TaskModel(TaskBase, table=True):
    __tablename__ = "tasks"  # pyright: ignore[reportUnannotatedClassAttribute, reportAssignmentType]
    id: int | None = Field(default=None, primary_key=True, index=True)
    # Foreign key referencing the User model
    user_id: int | None = Field(default=None, foreign_key="users.id")
    # Define the relationship to the User model
    user: UserModel | None = cast(UserModel, Relationship(back_populates="tasks"))
