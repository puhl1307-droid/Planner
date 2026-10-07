from datetime import date

from app.models.task import Task
from app.models.idea_note import IdeaNote, IdeaNoteStatus


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


    def convert_idea_to_task(
        self,
        idea: IdeaNote,
        title,
        area_id,
        focus_requirement,
        status,
        description=None,
        deadline=None,
        estimated_minutes=None,
    ):
        if idea.status == IdeaNoteStatus.CONVERTED:
            raise ValueError(
                "Die IdeaNote wurde bereits in einen Task umgewandelt."
            )

        task = self.create_task(
            title=title,
            area_id=area_id,
            focus_requirement=focus_requirement,
            status=status,
            description=description,
            deadline=deadline,
            estimated_minutes=estimated_minutes,
        )

        idea.status = IdeaNoteStatus.CONVERTED
        idea.converted_task_id = task.id

        return task


    def next_task_id(self):
        if not self.tasks:
            return 1

        return max(
            task.id for task in self.tasks
        ) + 1