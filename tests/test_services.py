from datetime import datetime

import unittest

from app.models.focus_level import FocusLevel
from app.models.task import Task, TaskStatus
from app.models.idea_note import IdeaNote, IdeaNoteStatus
from app.models.planning_block import PlanningBlock
from app.models.work_block import WorkBlock
from app.services.task_service import TaskService
from app.services.work_block_service import WorkBlockService
from app.services.planning_block_service import PlanningBlockService
from app.services.planning_validation_service import PlanningValidationService


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


class TestPlanningBlockService(unittest.TestCase):
    def test_create_planning_block(self):
        service = PlanningBlockService()

        planning_block = service.create_planning_block(
            task_id=1,
            start_at=datetime(2026, 10, 22, 9, 0),
            end_at=datetime(2026, 10, 22, 10, 30),
        )

        self.assertEqual(
            planning_block.id,
            1,
        )
        self.assertEqual(
            planning_block.task_id,
            1,
        )
        self.assertEqual(
            len(service.planning_blocks),
            1,
        )

    def test_unique_ids(self):
        service = PlanningBlockService()

        first = service.create_planning_block(
            task_id=1,
            start_at=datetime(2026, 10, 22, 9, 0),
            end_at=datetime(2026, 10, 22, 10, 0),
        )

        second = service.create_planning_block(
            task_id=2,
            start_at=datetime(2026, 10, 22, 10, 0),
            end_at=datetime(2026, 10, 22, 11, 0),
        )

        self.assertEqual(first.id, 1)
        self.assertEqual(second.id, 2)

    def test_id_after_existing_planning_block(self):
        existing = PlanningBlock(
            id=7,
            task_id=1,
            start_at=datetime(2026, 10, 22, 9, 0),
            end_at=datetime(2026, 10, 22, 10, 0),
        )

        service = PlanningBlockService(
            [existing]
        )

        new_block = service.create_planning_block(
            task_id=2,
            start_at=datetime(2026, 10, 22, 10, 0),
            end_at=datetime(2026, 10, 22, 11, 0),
        )

        self.assertEqual(
            new_block.id,
            8,
        )

    def test_invalid_time_range_is_not_saved(self):
        service = PlanningBlockService()

        with self.assertRaises(ValueError):
            service.create_planning_block(
                task_id=1,
                start_at=datetime(2026, 10, 22, 11, 0),
                end_at=datetime(2026, 10, 22, 10, 0),
            )

        self.assertEqual(
            len(service.planning_blocks),
            0,
        )

    def test_optional_work_block_assignment(self):
        service = PlanningBlockService()

        planning_block = service.create_planning_block(
            task_id=1,
            start_at=datetime(2026, 10, 22, 9, 0),
            end_at=datetime(2026, 10, 22, 10, 0),
            work_block_id=4,
        )

        self.assertEqual(
            planning_block.work_block_id,
            4,
        )


class TestPlanningValidationService(unittest.TestCase):
    def setUp(self):
        self.service = PlanningValidationService()

        self.task = Task(
            id=1,
            title="SEO optimieren",
            area_id=1,
            focus_requirement=FocusLevel.MEDIUM,
        )

        self.work_block = WorkBlock(
            id=1,
            title="Fokusarbeit",
            start_at=datetime(2026, 10, 22, 8, 0),
            end_at=datetime(2026, 10, 22, 12, 0),
            focus_level=FocusLevel.HIGH,
        )

    def test_valid_planning_block_has_no_warnings(self):
        planning_block = PlanningBlock(
            id=1,
            task_id=1,
            start_at=datetime(2026, 10, 22, 9, 0),
            end_at=datetime(2026, 10, 22, 10, 0),
            work_block_id=1,
        )

        warnings = self.service.validate_planning_block(
            planning_block=planning_block,
            planning_blocks=[planning_block],
            work_blocks=[self.work_block],
            tasks=[self.task],
        )

        self.assertEqual(warnings, [])

    def test_warning_if_work_block_does_not_exist(self):
        planning_block = PlanningBlock(
            id=1,
            task_id=1,
            start_at=datetime(2026, 10, 22, 9, 0),
            end_at=datetime(2026, 10, 22, 10, 0),
            work_block_id=99,
        )

        warnings = self.service.validate_planning_block(
            planning_block=planning_block,
            planning_blocks=[planning_block],
            work_blocks=[self.work_block],
            tasks=[self.task],
        )

        self.assertIn(
            "Der zugeordnete WorkBlock existiert nicht.",
            warnings,
        )

    def test_warning_if_planning_block_is_outside_work_block(self):
        planning_block = PlanningBlock(
            id=1,
            task_id=1,
            start_at=datetime(2026, 10, 22, 11, 0),
            end_at=datetime(2026, 10, 22, 13, 0),
            work_block_id=1,
        )

        warnings = self.service.validate_planning_block(
            planning_block=planning_block,
            planning_blocks=[planning_block],
            work_blocks=[self.work_block],
            tasks=[self.task],
        )

        self.assertIn(
            "Der PlanningBlock liegt nicht vollständig innerhalb des WorkBlocks.",
            warnings,
        )

    def test_warning_if_task_requires_more_focus_than_work_block_provides(self):
        high_focus_task = Task(
            id=2,
            title="Komplexe Planung",
            area_id=1,
            focus_requirement=FocusLevel.HIGH,
        )

        low_focus_work_block = WorkBlock(
            id=2,
            title="Laden geöffnet",
            start_at=datetime(2026, 10, 22, 8, 0),
            end_at=datetime(2026, 10, 22, 12, 0),
            focus_level=FocusLevel.LOW,
        )

        planning_block = PlanningBlock(
            id=1,
            task_id=2,
            start_at=datetime(2026, 10, 22, 9, 0),
            end_at=datetime(2026, 10, 22, 10, 0),
            work_block_id=2,
        )

        warnings = self.service.validate_planning_block(
            planning_block=planning_block,
            planning_blocks=[planning_block],
            work_blocks=[low_focus_work_block],
            tasks=[high_focus_task],
        )

        self.assertIn(
            "Der Fokusbedarf des Tasks ist höher als der verfügbare Fokus im WorkBlock.",
            warnings,
        )

    def test_warning_if_planning_blocks_overlap(self):
        existing_block = PlanningBlock(
            id=1,
            task_id=1,
            start_at=datetime(2026, 10, 22, 9, 0),
            end_at=datetime(2026, 10, 22, 10, 30),
            work_block_id=1,
        )

        new_block = PlanningBlock(
            id=2,
            task_id=1,
            start_at=datetime(2026, 10, 22, 10, 0),
            end_at=datetime(2026, 10, 22, 11, 0),
            work_block_id=1,
        )

        warnings = self.service.validate_planning_block(
            planning_block=new_block,
            planning_blocks=[
                existing_block,
                new_block,
            ],
            work_blocks=[self.work_block],
            tasks=[self.task],
        )

        self.assertIn(
            "Der PlanningBlock überschneidet sich mit einem anderen PlanningBlock.",
            warnings,
        )

    def test_touching_planning_blocks_do_not_overlap(self):
        first_block = PlanningBlock(
            id=1,
            task_id=1,
            start_at=datetime(2026, 10, 22, 9, 0),
            end_at=datetime(2026, 10, 22, 10, 0),
            work_block_id=1,
        )

        second_block = PlanningBlock(
            id=2,
            task_id=1,
            start_at=datetime(2026, 10, 22, 10, 0),
            end_at=datetime(2026, 10, 22, 11, 0),
            work_block_id=1,
        )

        warnings = self.service.validate_planning_block(
            planning_block=second_block,
            planning_blocks=[
                first_block,
                second_block,
            ],
            work_blocks=[self.work_block],
            tasks=[self.task],
        )

        self.assertNotIn(
            "Der PlanningBlock überschneidet sich mit einem anderen PlanningBlock.",
            warnings,
        )


if __name__ == "__main__":
    unittest.main()