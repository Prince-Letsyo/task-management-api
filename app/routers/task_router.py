from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas import TaskCreate, Task, TaskUpdate
from app.services import TaskService
from app.dependencies import get_task_service


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=List[Task])
async def read_tasks(
    task_service: TaskService = Depends(get_task_service),
):
    return await task_service.get_all_tasks()
