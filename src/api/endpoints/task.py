from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas import Task, TaskCreate, TaskError
from src.services import TaskService


task_router = APIRouter()
task_service = TaskService()


@task_router.get(
    "/tasks/{task_id}",
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
            detail=TaskError(error=f"Task with id {task_id} not found").dict(),
        )
    return task


@task_router.post("/tasks", status_code=status.HTTP_201_CREATED, response_model=Task)
def create_task(
    task_create: TaskCreate, service: TaskService = Depends(lambda: task_service)
):
    return service.create_task(task_create)


@task_router.get("/tasks", response_model=list[Task])
def get_all_tasks(service: TaskService = Depends(lambda: task_service)):
    return service.get_all_tasks()
