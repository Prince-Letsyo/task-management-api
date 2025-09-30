from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas import TaskCreate, Task, TaskUpdate
from app.services import TaskService
from app.dependencies import get_task_service


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[Task])
async def read_tasks(
    task_service: TaskService = Depends(get_task_service),
):
    all_task = await task_service.get_all_tasks()
    return all_task


@router.get(
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=Task,
    responses={
        status.HTTP_200_OK: {
            "model": Task,
            "description": "Item retrieved successfully",
        },
    },
)
async def read_task_by_id(
    task_id: int,
    task_service: TaskService = Depends(get_task_service),
) -> Task:
    task = await task_service.get_task_by_id(task_id=task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )
    return task


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Task,
    responses={
        status.HTTP_201_CREATED: {
            "model": Task,
            "description": "Item created successfully",
        }
    },
)
async def create_post(
    task_create: TaskCreate, task_service: TaskService = Depends(get_task_service)
) -> Task:
    new_task = await task_service.create_task(task_create=task_create)
    return new_task


@router.put(
    "/{task_id}",
    response_model=Task,
    responses={
        status.HTTP_200_OK: {
            "model": Task,
            "description": "Item updated successfully",
        },
    },
)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    task_service: TaskService = Depends(get_task_service),
):
    updated_task = await task_service.update_task(
        task_id=task_id, task_update=task_update
    )
    if updated_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )
    return updated_task


@router.patch(
    "/{task_id}",
    response_model=Task,
    responses={
        status.HTTP_200_OK: {
            "model": Task,
            "description": "Item partially updated successfully",
        },
    },
)
async def partial_update_task(
    task_id: int,
    task_update: TaskUpdate,
    task_service: TaskService = Depends(get_task_service),
):
    partial_updated_task = await task_service.update_task(
        task_id=task_id, task_update=task_update
    )
    if partial_updated_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )
    return partial_updated_task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service),
):
    success = await task_service.delete_task(task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )
