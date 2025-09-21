from .. import models, schemas


class TaskService:
    def get_task_by_id(self, task_id: int) -> schemas.Task | None:
        for task in models.tasks:
            if task.id == task_id:
                return schemas.Task.from_orm(task)
        return None

    def create_task(self, task_create: schemas.TaskCreate) -> schemas.Task:
        new_id = max(task.id for task in models.tasks) + 1 if models.tasks else 1
        new_task = models.Task(
            id=new_id, title=task_create.title, description=task_create.description
        )
        models.tasks.append(new_task)
        return schemas.Task.from_orm(new_task)

    def get_all_tasks(
        self,
    ) -> list[schemas.Task]:
        return [schemas.Task.from_orm(task) for task in models.tasks]

    def update_task(
        self, task_id: int, task_update: schemas.TaskUpdate
    ) -> schemas.Task | None:
        for task in models.tasks:
            if task.id == task_id:
                if task_update.title is not None:
                    task.title = task_update.title
                if task_update.description is not None:
                    task.description = task_update.description
                return schemas.Task.from_orm(task)
        return None

    def partial_update_task(
        self, task_id: int, task_update: schemas.TaskUpdate
    ) -> schemas.Task | None:
        return self.update_task(task_id, task_update)

    def delete_task(self, task_id: int) -> bool:
        for i, task in enumerate(models.tasks):
            if task.id == task_id:
                del models.tasks[i]
                return True
        return False
