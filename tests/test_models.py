import unittest
from datetime import date, datetime

from app.models.area import Area
from app.models.task import Task, TaskStatus
from app.models.focus_level import FocusLevel
from app.models.idea_note import IdeaNote, IdeaNoteStatus
from app.models.work_block import WorkBlock
from app.models.planning_block import PlanningBlock, PlanningBlockStatus
from app.models.event import Event


# --------------------------------------------------
# AREA
# --------------------------------------------------

class TestArea(unittest.TestCase):

    def test_valid_area(self):
        area = Area(
            id=1,
            name="Arbeit",
            color="#4285F4"
        )

        self.assertEqual(area.name, "Arbeit")
        self.assertEqual(area.color, "#4285F4")
        self.assertTrue(area.active)

    def test_created_at(self):
        area = Area(
            id=1,
            name="Privat",
            color="#00AA00"
        )

        self.assertIsInstance(area.created_at, datetime)


# --------------------------------------------------
# TASK
# --------------------------------------------------

class TestTask(unittest.TestCase):

    def test_valid_task(self):
        task = Task(
            id=1,
            title="SEO überarbeiten",
            area_id=1,
            focus_requirement=FocusLevel.HIGH
        )

        self.assertEqual(task.title, "SEO überarbeiten")
        self.assertEqual(task.area_id, 1)
        self.assertEqual(task.status, TaskStatus.IN_DEFINITION)

    def test_optional_fields(self):
        task = Task(
            id=1,
            title="Google Ads optimieren",
            area_id=1,
            focus_requirement=FocusLevel.MEDIUM,
            description="Kampagne überprüfen",
            deadline=date(2026, 11, 15),
            estimated_minutes=120
        )

        self.assertEqual(task.estimated_minutes, 120)
        self.assertEqual(task.deadline, date(2026, 11, 15))

    def test_empty_title(self):
        with self.assertRaises(ValueError):
            Task(
                id=2,
                title="",
                area_id=1,
                focus_requirement=FocusLevel.HIGH
            )

    def test_invalid_estimated_minutes(self):
        with self.assertRaises(ValueError):
            Task(
                id=3,
                title="Google Ads",
                area_id=1,
                focus_requirement=FocusLevel.MEDIUM,
                estimated_minutes=-30
            )

    def test_invalid_focus_level(self):
        with self.assertRaises(ValueError):
            Task(
                id=4,
                title="Test",
                area_id=1,
                focus_requirement="high"
            )

    def test_invalid_status(self):
        with self.assertRaises(ValueError):
            Task(
                id=5,
                title="Test",
                area_id=1,
                focus_requirement=FocusLevel.LOW,
                status="open"
            )


# --------------------------------------------------
# IDEA NOTE
# --------------------------------------------------

class TestIdeaNote(unittest.TestCase):

    def test_valid_idea_note(self):
        idea = IdeaNote(
            id=1,
            thought="Newsletter-Aktion überlegen"
        )

        self.assertEqual(
            idea.thought,
            "Newsletter-Aktion überlegen"
        )
        self.assertEqual(idea.status, IdeaNoteStatus.INBOX)

    def test_optional_fields(self):
        idea = IdeaNote(
            id=2,
            thought="Neue Produktidee",
            status=IdeaNoteStatus.SNOOZED,
            snoozed_until=date(2026, 11, 1)
        )

        self.assertEqual(idea.status, IdeaNoteStatus.SNOOZED)
        self.assertEqual(
            idea.snoozed_until,
            date(2026, 11, 1)
        )

    def test_created_at(self):
        idea = IdeaNote(
            id=3,
            thought="Testgedanke"
        )

        self.assertIsInstance(idea.created_at, datetime)


# --------------------------------------------------
# WORK BLOCK
# --------------------------------------------------

class TestWorkBlock(unittest.TestCase):

    def test_valid_work_block(self):
        block = WorkBlock(
            id=1,
            title="Fokusarbeit",
            start_at=datetime(2026, 10, 7, 8, 0),
            end_at=datetime(2026, 10, 7, 12, 0),
            focus_level=FocusLevel.HIGH
        )

        self.assertEqual(block.title, "Fokusarbeit")
        self.assertEqual(block.focus_level, FocusLevel.HIGH)

    def test_invalid_time_range(self):
        with self.assertRaises(ValueError):
            WorkBlock(
                id=2,
                title="Fokusarbeit",
                start_at=datetime(2026, 10, 7, 12, 0),
                end_at=datetime(2026, 10, 7, 8, 0),
                focus_level=FocusLevel.HIGH
            )

    def test_equal_start_end(self):
        with self.assertRaises(ValueError):
            WorkBlock(
                id=3,
                title="Test",
                start_at=datetime(2026, 10, 7, 9, 0),
                end_at=datetime(2026, 10, 7, 9, 0),
                focus_level=FocusLevel.LOW
            )


# --------------------------------------------------
# PLANNING BLOCK
# --------------------------------------------------

class TestPlanningBlock(unittest.TestCase):

    def test_valid_planning_block(self):
        block = PlanningBlock(
            id=1,
            task_id=1,
            start_at=datetime(2026, 10, 7, 9, 0),
            end_at=datetime(2026, 10, 7, 10, 30)
        )

        self.assertEqual(block.task_id, 1)
        self.assertIsNone(block.work_block_id)
        self.assertEqual(
            block.status,
            PlanningBlockStatus.PLANNED
        )

    def test_work_block_assignment(self):
        block = PlanningBlock(
            id=2,
            task_id=1,
            work_block_id=3,
            start_at=datetime(2026, 10, 7, 9, 0),
            end_at=datetime(2026, 10, 7, 11, 0)
        )

        self.assertEqual(block.work_block_id, 3)

    def test_invalid_time_range(self):
        with self.assertRaises(ValueError):
            PlanningBlock(
                id=3,
                task_id=1,
                start_at=datetime(2026, 10, 7, 12, 0),
                end_at=datetime(2026, 10, 7, 9, 0)
            )

    def test_invalid_actual_time_range(self):
        with self.assertRaises(ValueError):
            PlanningBlock(
                id=4,
                task_id=1,
                start_at=datetime(2026, 10, 7, 9, 0),
                end_at=datetime(2026, 10, 7, 10, 0),
                actual_start_at=datetime(2026, 10, 7, 11, 0),
                actual_end_at=datetime(2026, 10, 7, 10, 30)
            )

    def test_valid_actual_time_range(self):
        block = PlanningBlock(
            id=5,
            task_id=1,
            start_at=datetime(2026, 10, 7, 9, 0),
            end_at=datetime(2026, 10, 7, 10, 0),
            actual_start_at=datetime(2026, 10, 7, 9, 15),
            actual_end_at=datetime(2026, 10, 7, 10, 30)
        )

        actual_minutes = int(
            (
                block.actual_end_at - block.actual_start_at
            ).total_seconds() / 60
        )

        self.assertEqual(actual_minutes, 75)


# --------------------------------------------------
# EVENT
# --------------------------------------------------

class TestEvent(unittest.TestCase):

    def test_valid_event(self):
        event = Event(
            id=1,
            title="Lieferantengespräch",
            area_id=1,
            start_at=datetime(2026, 10, 7, 14, 0),
            end_at=datetime(2026, 10, 7, 15, 0)
        )

        self.assertEqual(event.title, "Lieferantengespräch")
        self.assertEqual(event.area_id, 1)
        self.assertIsNone(event.work_block_id)

    def test_work_block_assignment(self):
        event = Event(
            id=2,
            title="Besprechung",
            area_id=1,
            work_block_id=3,
            start_at=datetime(2026, 10, 7, 10, 0),
            end_at=datetime(2026, 10, 7, 11, 0)
        )

        self.assertEqual(event.work_block_id, 3)

    def test_invalid_time_range(self):
        with self.assertRaises(ValueError):
            Event(
                id=3,
                title="Ungültiger Termin",
                area_id=1,
                start_at=datetime(2026, 10, 7, 15, 0),
                end_at=datetime(2026, 10, 7, 14, 0)
            )


if __name__ == "__main__":
    unittest.main()