from sqlalchemy import Column, Enum, Integer, String
from app.db.db import Base


class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    status = Column(
        Enum("pending", "in-progress", "completed", name="task_status"),
        nullable=False,
        default="pending",
    )
