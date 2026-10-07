from datetime import datetime

import unittest

from app.models.focus_level import FocusLevel
from app.models.task import TaskStatus
from app.services.task_service import TaskService
from app.models.idea_note import IdeaNote, IdeaNoteStatus
from app.services.work_block_service import WorkBlockService


class TestTaskService(unittest.TestCase):

    def setUp(self):
        self.service = TaskService()

    def test_create_task(self):
        task = self.service.create_task(
            title="SEO überarbeiten",
            area_id=1,
            focus_requirement=FocusLevel.HIGH,
            status=TaskStatus.OPEN,
        )

        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "SEO überarbeiten")
        self.assertEqual(task.status, TaskStatus.OPEN)
        self.assertEqual(len(self.service.tasks), 1)

    def test_multiple_tasks_get_unique_ids(self):
        first = self.service.create_task(
            title="Task 1",
            area_id=1,
            focus_requirement=FocusLevel.LOW,
            status=TaskStatus.OPEN,
        )

        second = self.service.create_task(
            title="Task 2",
            area_id=1,
            focus_requirement=FocusLevel.MEDIUM,
            status=TaskStatus.OPEN,
        )

        self.assertEqual(first.id, 1)
        self.assertEqual(second.id, 2)

    def test_id_after_existing_tasks(self):
        self.service.create_task(
            title="Task 1",
            area_id=1,
            focus_requirement=FocusLevel.LOW,
            status=TaskStatus.OPEN,
        )

        task = self.service.create_task(
            title="Task 2",
            area_id=1,
            focus_requirement=FocusLevel.HIGH,
            status=TaskStatus.OPEN,
        )

        self.assertEqual(task.id, 2)

    def test_invalid_task_not_saved(self):
        with self.assertRaises(ValueError):
            self.service.create_task(
                title="",
                area_id=1,
                focus_requirement=FocusLevel.HIGH,
                status=TaskStatus.OPEN,
            )

        self.assertEqual(len(self.service.tasks), 0)

    def test_optional_fields(self):
        task = self.service.create_task(
            title="Google Ads optimieren",
            area_id=1,
            focus_requirement=FocusLevel.HIGH,
            status=TaskStatus.OPEN,
            description="Kampagne prüfen",
            estimated_minutes=120,
        )

        self.assertEqual(task.description, "Kampagne prüfen")
        self.assertEqual(task.estimated_minutes, 120)


    def test_convert_idea_to_task(self):
        idea = IdeaNote(
            id=1,
            thought="Newsletter planen",
        )

        task = self.service.convert_idea_to_task(
            idea=idea,
            title="Newsletter planen",
            area_id=1,
            focus_requirement=FocusLevel.MEDIUM,
            status=TaskStatus.OPEN,
        )

        self.assertEqual(task.title, "Newsletter planen")
        self.assertEqual(len(self.service.tasks), 1)

        self.assertEqual(
            idea.status,
            IdeaNoteStatus.CONVERTED,
        )

        self.assertEqual(
            idea.converted_task_id,
            task.id,
        )


    def test_converted_idea_cannot_be_converted_again(self):
        idea = IdeaNote(
            id=1,
            thought="Newsletter planen",
        )

        self.service.convert_idea_to_task(
            idea=idea,
            title="Newsletter planen",
            area_id=1,
            focus_requirement=FocusLevel.MEDIUM,
            status=TaskStatus.OPEN,
        )

        with self.assertRaises(ValueError):
            self.service.convert_idea_to_task(
                idea=idea,
                title="Newsletter nochmal",
                area_id=1,
                focus_requirement=FocusLevel.MEDIUM,
                status=TaskStatus.OPEN,
            )

        self.assertEqual(len(self.service.tasks), 1)


    def test_failed_conversion_does_not_change_idea(self):
        idea = IdeaNote(
            id=1,
            thought="Newsletter planen",
        )

        with self.assertRaises(ValueError):
            self.service.convert_idea_to_task(
                idea=idea,
                title="",
                area_id=1,
                focus_requirement=FocusLevel.MEDIUM,
                status=TaskStatus.OPEN,
            )

        self.assertEqual(
            idea.status,
            IdeaNoteStatus.INBOX,
        )

        self.assertIsNone(
            idea.converted_task_id
        )

        self.assertEqual(
            len(self.service.tasks),
            0,
        )


class TestWorkBlockService(unittest.TestCase):

    def setUp(self):
        self.service = WorkBlockService()

    def test_create_work_block(self):
        work_block = self.service.create_work_block(
            title="Fokusarbeit",
            start_at=datetime(2026, 10, 8, 8, 0),
            end_at=datetime(2026, 10, 8, 12, 0),
            focus_level=FocusLevel.HIGH,
        )

        self.assertEqual(work_block.id, 1)
        self.assertEqual(work_block.title, "Fokusarbeit")
        self.assertEqual(work_block.focus_level, FocusLevel.HIGH)
        self.assertEqual(len(self.service.work_blocks), 1)

    def test_multiple_work_blocks_get_unique_ids(self):
        first = self.service.create_work_block(
            title="Fokusarbeit",
            start_at=datetime(2026, 10, 8, 8, 0),
            end_at=datetime(2026, 10, 8, 10, 0),
            focus_level=FocusLevel.HIGH,
        )

        second = self.service.create_work_block(
            title="Laden geöffnet",
            start_at=datetime(2026, 10, 8, 10, 0),
            end_at=datetime(2026, 10, 8, 14, 0),
            focus_level=FocusLevel.LOW,
        )

        self.assertEqual(first.id, 1)
        self.assertEqual(second.id, 2)

    def test_id_after_existing_work_blocks(self):
        self.service.create_work_block(
            title="Block 1",
            start_at=datetime(2026, 10, 8, 8, 0),
            end_at=datetime(2026, 10, 8, 9, 0),
            focus_level=FocusLevel.MEDIUM,
        )

        work_block = self.service.create_work_block(
            title="Block 2",
            start_at=datetime(2026, 10, 8, 9, 0),
            end_at=datetime(2026, 10, 8, 10, 0),
            focus_level=FocusLevel.MEDIUM,
        )

        self.assertEqual(work_block.id, 2)

    def test_invalid_time_range_not_saved(self):
        with self.assertRaises(ValueError):
            self.service.create_work_block(
                title="Ungültiger Block",
                start_at=datetime(2026, 10, 8, 12, 0),
                end_at=datetime(2026, 10, 8, 8, 0),
                focus_level=FocusLevel.HIGH,
            )

        self.assertEqual(len(self.service.work_blocks), 0)

    def test_optional_description(self):
        work_block = self.service.create_work_block(
            title="Termin: Kollege XY",
            start_at=datetime(2026, 10, 8, 12, 0),
            end_at=datetime(2026, 10, 8, 16, 0),
            focus_level=FocusLevel.LOW,
            description="Laden ist geöffnet, deshalb nur eingeschränkter Fokus.",
        )

        self.assertEqual(
            work_block.description,
            "Laden ist geöffnet, deshalb nur eingeschränkter Fokus.",
        )


if __name__ == "__main__":
    unittest.main()