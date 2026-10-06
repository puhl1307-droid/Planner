from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum


class IdeaNoteStatus(Enum):
    INBOX = "inbox"
    SNOOZED = "snoozed"
    CONVERTED = "converted"
    DISCARDED = "discarded"


@dataclass
class IdeaNote:
    id: int
    thought: str

    status: IdeaNoteStatus = IdeaNoteStatus.INBOX
    created_at: datetime = field(default_factory=datetime.now)

    snoozed_until: date | None = None
    converted_task_id: int | None = None