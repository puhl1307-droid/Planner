from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum

from app.models.focus_level import FocusLevel


class TaskStatus(Enum):
    IN_DEFINITION = "in_definition"
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class Task:
    id: int
    title: str
    area_id: int
    focus_requirement: FocusLevel
    status: TaskStatus = TaskStatus.IN_DEFINITION

    description: str | None = None
    deadline: date | None = None
    estimated_minutes: int | None = None

    created_at: datetime = field(default_factory=datetime.now)


    def __post_init__(self):
        if not self.title.strip():
            raise ValueError("Ein Task benötigt einen Titel.")

        if self.estimated_minutes is not None:
            if self.estimated_minutes <= 0:
                raise ValueError(
                    "Der geschätzte Aufwand muss größer als 0 sein."
                )

        if not isinstance(self.focus_requirement, FocusLevel):
            raise ValueError("Ungültiger Fokusbedarf.")

        if not isinstance(self.status, TaskStatus):
            raise ValueError("Ungültiger Task-Status.")
