from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: str | None = None
    due_date: str | None = None  # ISO 8601 date string, optional


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int

    class Config:
        from_attributes = True


class TaskUpdate(TaskBase):
    title: str | None = None


class TaskError(BaseModel):
    error: str
