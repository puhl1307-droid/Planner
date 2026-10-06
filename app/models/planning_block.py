from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class PlanningBlockStatus(Enum):
    PLANNED = "planned"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class PlanningBlock:
    id: int
    task_id: int
    start_at: datetime
    end_at: datetime

    status: PlanningBlockStatus = PlanningBlockStatus.PLANNED

    work_block_id: int | None = None

    actual_start_at: datetime | None = None
    actual_end_at: datetime | None = None

    notes: str | None = None
    created_at: datetime = field(default_factory=datetime.now)


    def __post_init__(self):
        if self.end_at <= self.start_at:
            raise ValueError(
                "Das Ende muss nach dem Beginn liegen."
            )

        if (
            self.actual_start_at is not None
            and self.actual_end_at is not None
            and self.actual_end_at <= self.actual_start_at
        ):
            raise ValueError(
                "Das tatsächliche Ende muss nach dem Beginn liegen."
            )