from pydantic import BaseModel
from typing import List


class Task(BaseModel):
    id: int
    title: str
    description: str | None = None
    due_date: str | None = None  # ISO 8601 date string, optional


tasks: List["Task"] = [
    Task(id=1, title="Buy groceries", description="Milk, Bread, Eggs", due_date="2024-06-10"),
    Task(id=2, title="Finish report", description="Complete the annual financial report", due_date="2024-06-15"),
    Task(id=3, title="Call plumber", description=None, due_date=None),
]
