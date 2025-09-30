from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas import Task, TaskCreate, TaskError, TaskUpdate
from src.services import task_services
from sqlmodel import Session
from typing import Annotated
from src.core import get_session
from src.models import TaskModel

from pydantic import ValidationError

task_router = APIRouter()
# task_service = TaskService()


@task_router.get(
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=Task | TaskError,
    responses={
        status.HTTP_200_OK: {
            "model": Task,
            "description": "Item retrieved successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": TaskError,
            "description": "Item not found",
        },
    },
)
def get_task_by_id(task_id: int, session: Annotated[Session, Depends(get_session)]):
    task = task_services.get_task_by_id(task_id, session)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=TaskError(error=f"Task with id {task_id} not found").model_dump(),
        )
    return task


@task_router.post(
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
def create_task(
    task_create: TaskCreate, session: Annotated[Session, Depends(get_session)]
):
    return task_services.create_task(task_create, session)


@task_router.get("/", response_model=list[Task])
def get_all_tasks(session: Annotated[Session, Depends(get_session)]):
    return task_services.get_all_tasks(session=session)


@task_router.put(
    "/{task_id}",
    response_model=Task | TaskError,
    responses={
        status.HTTP_200_OK: {
            "model": Task,
            "description": "Item updated successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": TaskError,
            "description": "Item not found",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": TaskError,
            "description": "Invalid attribute format",
        },
    },
)
def update_task(
    task_id: int,
    task_update: TaskUpdate | TaskError,
    session: Annotated[Session, Depends(get_session)],
):
    updated_task = task_services.update_task(task_id, task_update, session=session)
    if updated_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=TaskError(error=f"Task with id {task_id} not found").model_dump(),
        )
    return updated_task


@task_router.patch(
    "/{task_id}",
    response_model=Task | TaskError,
    responses={
        status.HTTP_200_OK: {
            "model": Task,
            "description": "Item partially updated successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": TaskError,
            "description": "Item not found",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": TaskError,
            "description": "Invalid attribute format",
        },
    },
)
def partial_update_task(
    task_id: int,
    task_update: TaskUpdate,
    session: Annotated[Session, Depends(get_session)],
):
    updated_task = task_services.partial_update_task(
        task_id, task_update, session=session
    )
    return updated_task


@task_router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": TaskError,
            "description": "Item not found",
        },
    },
    response_model=None,
)  # 204 No Content
def delete_task(
    task_id: int,
    session: Annotated[Session, Depends(get_session)],
):
    success = task_services.delete_task(task_id, session=session)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=TaskError(error=f"Task with id {task_id} not found").model_dump(),
        )
