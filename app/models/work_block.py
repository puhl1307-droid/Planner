from dataclasses import dataclass, field
from datetime import datetime

from app.models.focus_level import FocusLevel


@dataclass
class WorkBlock:
    id: int
    title: str
    start_at: datetime
    end_at: datetime
    focus_level: FocusLevel

    description: str | None = None
    created_at: datetime = field(default_factory=datetime.now)


    def __post_init__(self):
        if self.end_at <= self.start_at:
            raise ValueError(
                "Das Ende muss nach dem Beginn liegen."
            )