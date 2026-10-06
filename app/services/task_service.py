from datetime import date

from app.models.task import Task


class TaskService:
    def __init__(self, tasks: list[Task] | None = None):
        self.tasks = tasks or []

    def create_task(
        self,
        title,
        area_id,
        focus_requirement,
        status,
        description=None,
        deadline: date | None = None,
        estimated_minutes: int | None = None,
    ):
        task = Task(
            id=self.next_task_id(),
            title=title,
            description=description,
            area_id=area_id,
            focus_requirement=focus_requirement,
            status=status,
            estimated_minutes=estimated_minutes,
            deadline=deadline,
        )

        self.tasks.append(task)

        return task

    def next_task_id(self):
        if not self.tasks:
            return 1

        return max(
            task.id for task in self.tasks
        ) + 1