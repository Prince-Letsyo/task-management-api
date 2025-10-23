# app/models/task.py
from sqlmodel import Enum, SQLModel, Field
import enum
from pydantic import ConfigDict


# Define the Enum for task status
class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"


# Base model for shared fields
class TaskBase(SQLModel):
    title: str | None = Field(index=True, nullable=False)
    description: str | None = Field(default=None, nullable=True)
    status: TaskStatus = Field(
        default=TaskStatus.PENDING,
        sa_type=Enum(enums=TaskStatus),  # pyright: ignore[reportArgumentType]
        nullable=False,
    )

    model_config: ConfigDict = (  # pyright: ignore[reportIncompatibleVariableOverride]
        ConfigDict(from_attributes=True)
    )


# Model for creating tasks (used in POST requests)
class TaskCreate(TaskBase):
    pass


# Model for updating tasks (used in PUT/PATCH requests)
class TaskUpdate(TaskBase):
    pass


# Model for error responses
class TaskError(SQLModel):
    error: str
