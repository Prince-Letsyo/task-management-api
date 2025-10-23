from fastapi import Depends, Request, status
from typing import cast
from app.routers.base import CustomRouter
from app.schemas import TaskCreate, Task, TaskUpdate
from app.services import TaskService
from app.core import UnauthorizedException, get_task_service
from app.utils.auth import JWTPayload

router: CustomRouter = CustomRouter(prefix="/tasks", tags=["tasks"])


def require_auth(request: Request) -> JWTPayload:
    if request.state.user is None:  # pyright: ignore[reportAny]
        raise UnauthorizedException()
    return cast(JWTPayload, request.state.user)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=list[Task],
    dependencies=[
        Depends(dependency=require_auth),
    ],
)
async def read_tasks(
    request: Request,
    task_service: TaskService = Depends(
        dependency=get_task_service
    ),  # pyright: ignore[reportCallInDefaultInitializer]
) -> list[Task]:
    user: JWTPayload = cast(JWTPayload, request.state.user)
    all_task: list[Task] = await task_service.get_all_tasks(username=user["username"])
    return all_task


@router.get(
    path="/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=Task,
    responses={
        status.HTTP_200_OK: {
            "model": Task,
            "description": "Item retrieved successfully",
        },
    },
    dependencies=[
        Depends(dependency=require_auth),
    ],
)
async def read_task_by_id(
    request: Request,
    task_id: int,
    task_service: TaskService = Depends(  # pyright: ignore[reportCallInDefaultInitializer]
        dependency=get_task_service
    ),
) -> Task:
    user: JWTPayload = cast(JWTPayload, request.state.user)
    task: Task = await task_service.get_task_by_id(
        username=user["username"], task_id=task_id
    )
    return task


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=Task,
    responses={
        status.HTTP_201_CREATED: {
            "model": Task,
            "description": "Item created successfully",
        }
    },
    dependencies=[
        Depends(dependency=require_auth),
    ],
)
async def create_post(
    request: Request,
    task_create: TaskCreate,
    task_service: TaskService = Depends(  # pyright: ignore[reportCallInDefaultInitializer]
        dependency=get_task_service
    ),
) -> Task:
    user: JWTPayload = cast(JWTPayload, request.state.user)
    new_task: Task = await task_service.create_task(
        username=user["username"], task_create=task_create
    )
    return new_task


@router.put(
    path="/{task_id}",
    response_model=Task,
    responses={
        status.HTTP_200_OK: {
            "model": Task,
            "description": "Item updated successfully",
        },
    },
    dependencies=[
        Depends(dependency=require_auth),
    ],
)
async def update_task(
    request: Request,
    task_id: int,
    task_update: TaskUpdate,
    task_service: TaskService = Depends(  # pyright: ignore[reportCallInDefaultInitializer]
        dependency=get_task_service
    ),
) -> Task:
    user: JWTPayload = cast(JWTPayload, request.state.user)
    updated_task: Task = await task_service.update_task(
        username=user["username"], task_id=task_id, task_update=task_update
    )
    return updated_task


@router.patch(
    path="/{task_id}",
    response_model=Task,
    responses={
        status.HTTP_200_OK: {
            "model": Task,
            "description": "Item partially updated successfully",
        },
    },
    dependencies=[
        Depends(dependency=require_auth),
    ],
)
async def partial_update_task(
    request: Request,
    task_id: int,
    task_update: TaskUpdate,
    task_service: TaskService = Depends(  # pyright: ignore[reportCallInDefaultInitializer]
        dependency=get_task_service
    ),
) -> Task:
    user: JWTPayload = cast(JWTPayload, request.state.user)
    partial_updated_task: Task = await task_service.update_task(
        username=user["username"], task_id=task_id, task_update=task_update
    )
    return partial_updated_task


@router.delete(
    path="/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(require_auth),
    ],
)
async def delete_task(
    request: Request,
    task_id: int,
    task_service: TaskService = Depends(  # pyright: ignore[reportCallInDefaultInitializer]
        dependency=get_task_service
    ),
) -> None:
    user: JWTPayload = cast(JWTPayload, request.state.user)
    _success: bool = await task_service.delete_task(
        username=user["username"], task_id=task_id
    )
