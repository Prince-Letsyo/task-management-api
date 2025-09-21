from pydantic import BaseModel
from typing import List


class Task(BaseModel):
    id: int
    title: str
    description: str | None = None


tasks: List["Task"] = [
    Task(id=1, title="Buy groceries", description="Milk, Bread, Eggs"),
    Task(id=2, title="Read book", description="Finish reading 'Atomic Habits'"),
    Task(id=3, title="Workout", description="30 minutes of cardio"),
]
