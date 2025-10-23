from fastapi import APIRouter, Depends, HTTPException, Request, status
from typing import cast
from app.schemas import TaskCreate, Task, TaskUpdate
from app.services import TaskService
from app.dependencies import get_task_service
from app.utils.auth import JWTPayload

router = APIRouter(prefix="/tasks", tags=["tasks"])


def require_auth(request: Request) -> JWTPayload:
    if request.state.user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing JWT"
        )
    return cast(JWTPayload, request.state.user)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[Task],
    dependencies=[
        Depends(require_auth),
    ],
)
async def read_tasks(
    request: Request,
    task_service: TaskService = Depends(get_task_service),
):
    user = cast(JWTPayload, request.state.user)
    all_task = await task_service.get_all_tasks(username=user["username"])
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
    dependencies=[
        Depends(require_auth),
    ],
)
async def read_task_by_id(
    request: Request,
    task_id: int,
    task_service: TaskService = Depends(get_task_service),
) -> Task:
    user = cast(JWTPayload, request.state.user)
    task = await task_service.get_task_by_id(username=user["username"], task_id=task_id)
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
    dependencies=[
        Depends(require_auth),
    ],
)
async def create_post(
    request: Request,
    task_create: TaskCreate,
    task_service: TaskService = Depends(get_task_service),
) -> Task:
    user = cast(JWTPayload, request.state.user)
    new_task = await task_service.create_task(
        username=user["username"], task_create=task_create
    )
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
    dependencies=[
        Depends(require_auth),
    ],
)
async def update_task(
    request: Request,
    task_id: int,
    task_update: TaskUpdate,
    task_service: TaskService = Depends(get_task_service),
):
    user = cast(JWTPayload, request.state.user)
    updated_task = await task_service.update_task(
        username=user["username"], task_id=task_id, task_update=task_update
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
    dependencies=[
        Depends(require_auth),
    ],
)
async def partial_update_task(
    request: Request,
    task_id: int,
    task_update: TaskUpdate,
    task_service: TaskService = Depends(get_task_service),
):
    user = cast(JWTPayload, request.state.user)
    partial_updated_task = await task_service.update_task(
        username=user["username"], task_id=task_id, task_update=task_update
    )
    return partial_updated_task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(require_auth),
    ],
)
async def delete_task(
    request: Request,
    task_id: int,
    task_service: TaskService = Depends(get_task_service),
):
    user = cast(JWTPayload, request.state.user)
    success = await task_service.delete_task(username=user["username"], task_id=task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )
