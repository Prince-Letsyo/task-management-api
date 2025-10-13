# app/models/task.py
from sqlmodel import SQLModel, Field, Enum
from typing import Optional
import enum
from pydantic import ConfigDict


# Define the Enum for task status
class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"


# Base model for shared fields
class TaskBase(SQLModel):
    title: str = Field(index=True, nullable=False)
    description: Optional[str] = Field(default=None, nullable=True)
    status: TaskStatus = Field(
        default=TaskStatus.PENDING, sa_type=Enum(TaskStatus), nullable=False
    )

    model_config = ConfigDict(from_attributes=True)


# Model for creating tasks (used in POST requests)
class TaskCreate(TaskBase):
    pass


# Model for updating tasks (used in PUT/PATCH requests)
class TaskUpdate(TaskBase):
    title: Optional[str] = Field(default=None, nullable=True)
    description: Optional[str] = Field(default=None, nullable=True)
    status: Optional[TaskStatus] = Field(
        default=None, sa_type=Enum(TaskStatus), nullable=True
    )


# Model for error responses
class TaskError(SQLModel):
    error: str
