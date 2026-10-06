from datetime import date

from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from app.models.task import Task
from app.dialogs.task_dialog import TaskDialog
from app.idea_note_panel import IdeaNotePanel
from app.models.idea_note import IdeaNoteStatus
from app.services.task_service import TaskService


class TaskPanel(QFrame):
    def __init__(
        self,
        tasks: list[Task] | None = None,
        areas=None,
    ):
        super().__init__()

        self.areas = areas or []
        self.tasks = tasks or []

        self.task_service = TaskService(self.tasks)

        self.setFixedWidth(320)
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(12)

        title = QLabel("Tasks")
        title.setStyleSheet(
            "font-size: 18px; font-weight: 600;"
        )

        open_overview_button = QPushButton("Tasks & Termine")
        open_overview_button.setMinimumHeight(38)

        add_button = QPushButton("+ Task")
        add_button.setMinimumHeight(38)

        add_button.clicked.connect(
            self.open_task_dialog
        )

        self.layout.addWidget(title)
        self.layout.addWidget(open_overview_button)
        self.layout.addWidget(add_button)

        self.layout.addSpacing(16)

        self.idea_panel = IdeaNotePanel()

        self.idea_panel.idea_conversion_requested.connect(
            self.convert_idea_to_task
        )

        self.layout.addWidget(self.idea_panel)

        self.layout.addSpacing(16)

        task_container = QFrame()

        self.task_list_layout = QVBoxLayout(task_container)
        self.task_list_layout.setContentsMargins(0, 0, 0, 0)
        self.task_list_layout.setSpacing(6)

        self.layout.addWidget(task_container)

        self.render_tasks()

        self.layout.addStretch()


    def render_tasks(self):
        for task in self.tasks:
            self.add_task_widget(task)


    def add_task_widget(self, task):
        task_frame = QFrame()

        task_layout = QVBoxLayout(task_frame)
        task_layout.setContentsMargins(0, 6, 0, 6)
        task_layout.setSpacing(3)

        title_label = QLabel(task.title)
        title_label.setWordWrap(True)

        status_label = QLabel(
            f"Status: {task.status.value}"
        )

        focus_label = QLabel(
            f"Fokus: {task.focus_requirement.value}"
        )

        task_layout.addWidget(title_label)
        task_layout.addWidget(status_label)
        task_layout.addWidget(focus_label)

        self.task_list_layout.addWidget(task_frame)

    def open_task_dialog(self):
        dialog = TaskDialog(
            areas=self.areas,
            parent=self,
        )

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        title = dialog.title_input.text().strip()

        if not title:
            return

        description = (
            dialog.description_input
            .toPlainText()
            .strip()
            or None
        )

        estimated_minutes = (
            dialog.duration_input.value()
            or None
        )

        deadline = None

        if dialog.deadline_enabled.isChecked():
            selected_date = dialog.deadline_input.date()

            deadline = date(
                selected_date.year(),
                selected_date.month(),
                selected_date.day(),
            )

        new_task = self.task_service.create_task(
            title=title,
            description=description,
            area_id=dialog.area_input.currentData(),
            focus_requirement=dialog.focus_input.currentData(),
            status=dialog.status_input.currentData(),
            estimated_minutes=estimated_minutes,
            deadline=deadline,
        )

        self.add_task_widget(new_task)


    def convert_idea_to_task(self, idea, idea_frame):
        dialog = TaskDialog(
            areas=self.areas,
            parent=self,
        )

        dialog.title_input.setText(idea.thought)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        title = dialog.title_input.text().strip()

        if not title:
            return

        description = (
            dialog.description_input
            .toPlainText()
            .strip()
            or None
        )

        estimated_minutes = (
            dialog.duration_input.value()
            or None
        )

        deadline = None

        if dialog.deadline_enabled.isChecked():
            selected_date = dialog.deadline_input.date()

            deadline = date(
                selected_date.year(),
                selected_date.month(),
                selected_date.day(),
            )

        new_task = self.task_service.create_task(
            title=title,
            description=description,
            area_id=dialog.area_input.currentData(),
            focus_requirement=dialog.focus_input.currentData(),
            status=dialog.status_input.currentData(),
            estimated_minutes=estimated_minutes,
            deadline=deadline,
        )

        self.add_task_widget(new_task)

        idea.status = IdeaNoteStatus.CONVERTED
        idea.converted_task_id = new_task.id

        idea_frame.hide()