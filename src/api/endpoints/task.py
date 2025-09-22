from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas import Task, TaskCreate, TaskError, TaskUpdate
from src.services import TaskService


task_router = APIRouter()
task_service = TaskService()


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
def get_task_by_id(task_id: int, service: TaskService = Depends(lambda: task_service)):
    task = service.get_task_by_id(task_id)
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
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": TaskError,
            "description": "Invalid attribute format",
        },
    },
)
def create_task(
    task_create: TaskCreate, service: TaskService = Depends(lambda: task_service)
):
    task = service.create_task(task_create)
    if task is ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=TaskError(error=f"Task with invalid date format").model_dump(),
        )
    return task


@task_router.get("/", response_model=list[Task])
def get_all_tasks(service: TaskService = Depends(lambda: task_service)):
    return service.get_all_tasks()


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
    service: TaskService = Depends(lambda: task_service),
):
    updated_task = service.update_task(task_id, task_update)
    if updated_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=TaskError(error=f"Task with id {task_id} not found").model_dump(),
        )
    elif update_task is ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=TaskError(error=f"Task with invalid date format").model_dump(),
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
    service: TaskService = Depends(lambda: task_service),
):
    updated_task = service.partial_update_task(task_id, task_update)
    if updated_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=TaskError(error=f"Task with id {task_id} not found").model_dump(),
        )
    elif update_task is ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=TaskError(error=f"Task with invalid date format").model_dump(),
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
def delete_task(task_id: int, service: TaskService = Depends(lambda: task_service)):
    success = service.delete_task(task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=TaskError(error=f"Task with id {task_id} not found").model_dump(),
        )
    return None
