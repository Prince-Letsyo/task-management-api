from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
    title: str
    description: str | None = None
    due_date: str | None = None  # ISO 8601 date string, optional
    model_config = ConfigDict(from_attributes=True)


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int


class TaskUpdate(TaskBase):
    title: str | None = None


class TaskError(BaseModel):
    error: str
