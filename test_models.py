from datetime import datetime

from app.models.area import Area
from app.models.task import Task, TaskStatus
from app.models.focus_level import FocusLevel
from app.models.idea_note import IdeaNote
from app.models.work_block import WorkBlock
from app.models.planning_block import PlanningBlock
from app.models.event import Event


area = Area(
    id=1,
    name="Arbeit",
    color="#4285F4"
)

task = Task(
    id=1,
    title="SEO-Landingpage überarbeiten",
    area_id=area.id,
    focus_requirement=FocusLevel.HIGH,
    status=TaskStatus.OPEN,
    estimated_minutes=120
)

idea = IdeaNote(
    id=1,
    thought="Newsletter-Aktion für November überlegen"
)

work_block = WorkBlock(
    id=1,
    title="Fokusarbeit",
    start_at=datetime(2026, 10, 7, 8, 0),
    end_at=datetime(2026, 10, 7, 12, 0),
    focus_level=FocusLevel.HIGH
)

planning_block = PlanningBlock(
    id=1,
    task_id=1,
    work_block_id=1,
    start_at=datetime(2026, 10, 7, 9, 0),
    end_at=datetime(2026, 10, 7, 10, 30)
)

event = Event(
    id=1,
    title="Lieferantengespräch",
    area_id=1,
    start_at=datetime(2026, 10, 7, 14, 0),
    end_at=datetime(2026, 10, 7, 15, 0)
)

print(area)
print(task)
print(idea)
print(work_block)
print(planning_block)
print(event)

try:
    invalid_task = Task(
        id=2,
        title="",
        area_id=1,
        focus_requirement=FocusLevel.HIGH
    )

    print("FEHLER: Ungültiger Task wurde akzeptiert.")

except ValueError as error:
    print(f"Validierung erfolgreich: {error}")