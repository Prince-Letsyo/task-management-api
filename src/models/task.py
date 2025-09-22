from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import date


class Task(BaseModel):
    id: int
    title: str
    description: str | None = None
    due_date: Optional[date] = None   # ISO 8601 date string, optional

    @field_validator("due_date", mode="before")
    def validate_iso_date(cls, v):
        if v is None:
            return v
        try:
            return v
        except ValueError:
            raise ValueError("Date must follow ISO 8601 format: YYYY-MM-DD")



tasks: List["Task"] = [
    Task(
        id=1,
        title="Buy groceries",
        description="Milk, Bread, Eggs",
        due_date="2024-06-10",
    ),
    Task(
        id=2,
        title="Finish report",
        description="Complete the annual financial report",
        due_date="2024-06-15",
    ),
    Task(id=3, title="Call plumber", description=None, due_date=None),
]
