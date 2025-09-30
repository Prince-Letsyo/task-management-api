from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from datetime import date


class TaskBase(BaseModel):
    title: str
    description: str | None = None
    due_date: Optional[date] = None  # ISO 8601 date string, optional
    model_config = ConfigDict(from_attributes=True)

    @field_validator("due_date", mode="before")
    def validate_iso_date(cls, v):
        if v is None:
            return v
        try:
            return v
        except ValueError:
            raise ValueError("Date must follow ISO 8601 format: YYYY-MM-DD")


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int


class TaskUpdate(TaskBase):
    title: str | None = None


class TaskError(BaseModel):
    error: str
