from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Area:
    id: int
    name: str
    color: str
    active: bool = True
    created_at: datetime = field(default_factory=datetime.now)