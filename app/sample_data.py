from datetime import date

from app.models.focus_level import FocusLevel
from app.models.task import Task, TaskStatus
from app.models.area import Area


def create_sample_areas():
    return [
        Area(
            id=1,
            name="Arbeit",
            color="#4285F4",
        ),
        Area(
            id=2,
            name="Privat",
            color="#34A853",
        ),
    ]


def create_sample_tasks():
    return [
        Task(
            id=1,
            title="SEO-Text überarbeiten",
            area_id=1,
            focus_requirement=FocusLevel.HIGH,
            status=TaskStatus.OPEN,
            estimated_minutes=90,
        ),
        Task(
            id=2,
            title="Rechnungen prüfen",
            area_id=1,
            focus_requirement=FocusLevel.LOW,
            status=TaskStatus.OPEN,
            estimated_minutes=30,
        ),
        Task(
            id=3,
            title="Newsletter vorbereiten",
            area_id=1,
            focus_requirement=FocusLevel.MEDIUM,
            status=TaskStatus.IN_DEFINITION,
            deadline=date(2026, 10, 15),
        ),
    ]