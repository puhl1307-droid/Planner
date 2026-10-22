from datetime import datetime, timedelta

from PySide6.QtWidgets import (
    QComboBox,
    QDateTimeEdit,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QMessageBox,
    QVBoxLayout,
)


class PlanningBlockDialog(QDialog):
    def __init__(
        self,
        tasks,
        work_blocks,
        parent=None,
    ):
        super().__init__(parent)

        self.tasks = tasks
        self.work_blocks = work_blocks

        self.setWindowTitle("PlanningBlock erstellen")
        self.resize(420, 260)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        form_layout = QFormLayout()

        self.task_input = QComboBox()

        for task in self.tasks:
            self.task_input.addItem(
                task.title,
                task.id,
            )

        self.start_input = QDateTimeEdit()
        self.start_input.setCalendarPopup(True)
        self.start_input.setDisplayFormat(
            "dd.MM.yyyy HH:mm"
        )

        self.end_input = QDateTimeEdit()
        self.end_input.setCalendarPopup(True)
        self.end_input.setDisplayFormat(
            "dd.MM.yyyy HH:mm"
        )

        now = datetime.now()

        self.start_input.setDateTime(
            now
        )

        self.end_input.setDateTime(
            now + timedelta(hours=1)
        )

        self.work_block_input = QComboBox()

        self.work_block_input.addItem(
            "Kein WorkBlock",
            None,
        )

        for work_block in self.work_blocks:
            self.work_block_input.addItem(
                work_block.title,
                work_block.id,
            )

        form_layout.addRow(
            "Task:",
            self.task_input,
        )

        form_layout.addRow(
            "Start:",
            self.start_input,
        )

        form_layout.addRow(
            "Ende:",
            self.end_input,
        )

        form_layout.addRow(
            "WorkBlock:",
            self.work_block_input,
        )

        layout.addLayout(form_layout)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(
            self.validate_and_accept
        )

        buttons.rejected.connect(
            self.reject
        )

        layout.addWidget(buttons)

    def validate_and_accept(self):
        if self.task_input.currentData() is None:
            QMessageBox.warning(
                self,
                "Fehlender Task",
                "Bitte wähle einen Task aus.",
            )
            return

        start_at = (
            self.start_input
            .dateTime()
            .toPython()
        )

        end_at = (
            self.end_input
            .dateTime()
            .toPython()
        )

        if end_at <= start_at:
            QMessageBox.warning(
                self,
                "Ungültiger Zeitraum",
                "Das Ende muss nach dem Start liegen.",
            )
            return

        if start_at.date() != end_at.date():
            QMessageBox.warning(
                self,
                "Ungültiger Zeitraum",
                "Ein PlanningBlock muss innerhalb eines Tages liegen.",
            )
            return

        self.accept()