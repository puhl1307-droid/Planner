from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QPlainTextEdit,
    QSpinBox,
    QVBoxLayout,
)

from app.models.focus_level import FocusLevel
from app.models.task import TaskStatus


class TaskDialog(QDialog):
    def __init__(self, areas, parent=None):
        super().__init__(parent)

        self.areas = areas

        self.setWindowTitle("Task erstellen")
        self.setMinimumWidth(450)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.title_input = QLineEdit()

        self.description_input = QPlainTextEdit()
        self.description_input.setMaximumHeight(100)

        self.area_input = QComboBox()

        for area in self.areas:
            self.area_input.addItem(area.name, area.id)

        self.focus_input = QComboBox()
        self.focus_input.addItem("Niedrig", FocusLevel.LOW)
        self.focus_input.addItem("Mittel", FocusLevel.MEDIUM)
        self.focus_input.addItem("Hoch", FocusLevel.HIGH)

        self.status_input = QComboBox()
        self.status_input.addItem(
            "In Definition",
            TaskStatus.IN_DEFINITION,
        )
        self.status_input.addItem(
            "Offen",
            TaskStatus.OPEN,
        )
        self.status_input.addItem(
            "In Bearbeitung",
            TaskStatus.IN_PROGRESS,
        )

        self.duration_input = QSpinBox()
        self.duration_input.setRange(0, 1440)
        self.duration_input.setSuffix(" Min.")
        self.duration_input.setSpecialValueText("Nicht festgelegt")

        self.deadline_enabled = QCheckBox("Deadline festlegen")

        self.deadline_input = QDateEdit()
        self.deadline_input.setCalendarPopup(True)
        self.deadline_input.setDate(QDate.currentDate())
        self.deadline_input.setEnabled(False)

        self.deadline_enabled.toggled.connect(
            self.deadline_input.setEnabled
        )

        form.addRow("Titel:", self.title_input)
        form.addRow("Beschreibung:", self.description_input)
        form.addRow("Bereich:", self.area_input)
        form.addRow("Fokusbedarf:", self.focus_input)
        form.addRow("Status:", self.status_input)
        form.addRow("Aufwand:", self.duration_input)
        form.addRow(self.deadline_enabled)
        form.addRow("Deadline:", self.deadline_input)

        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)