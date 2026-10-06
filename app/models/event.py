from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Event:
    id: int
    title: str
    start_at: datetime
    end_at: datetime
    area_id: int

    description: str | None = None
    work_block_id: int | None = None

    created_at: datetime = field(default_factory=datetime.now)


    def __post_init__(self):
        if self.end_at <= self.start_at:
            raise ValueError(
                "Das Ende muss nach dem Beginn liegen."
            )