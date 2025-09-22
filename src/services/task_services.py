from .. import models, schemas
from pydantic import ValidationError
from typing import Annotated
from sqlmodel import Session, select
from fastapi import Query


def get_task_by_id(task_id: int, session: Session) -> schemas.Task | None:
    task = session.get(models.TaskModel, task_id)
    if task:
        return schemas.Task.model_validate(task)
    return None


def create_task(task_create: schemas.TaskCreate, session: Session) -> schemas.Task:
    new_task = models.TaskModel.model_validate(task_create)
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return schemas.Task.model_validate(new_task)


def get_all_tasks(
    session: Session,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[schemas.Task]:
    all_tasks = session.exec(select(models.TaskModel).offset(offset).limit(limit)).all()
    return [schemas.Task.model_validate(task) for task in all_tasks]


def update_task(
    task_id: int, task_update: schemas.TaskUpdate, session: Session
) -> schemas.Task | None:
    new_task = session.get(models.TaskModel, task_id)
    if not new_task:
        return None
    task_data = task_update.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(new_task, key, value)
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return schemas.Task.model_validate(new_task)


def partial_update_task(
    task_id: int, task_update: schemas.TaskUpdate, session: Session
) -> schemas.Task | None:
    return update_task(task_id, task_update, session)


def delete_task(task_id: int, session: Session) -> bool:
    task = session.get(models.TaskModel, task_id)
    if not task:
        return False
    session.delete(task)
    session.commit()
    return True
