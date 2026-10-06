from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QCheckBox,
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)

from app.models.idea_note import IdeaNote, IdeaNoteStatus


class IdeaNoteDialog(QDialog):
    def __init__(self, idea: IdeaNote, parent=None):
        super().__init__(parent)

        self.idea = idea
        self.action = None

        self.setWindowTitle("Idee / Notiz")
        self.setMinimumWidth(450)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        thought_label = QLabel("Gedanke")

        self.thought_input = QTextEdit()
        self.thought_input.setPlainText(self.idea.thought)
        self.thought_input.setMaximumHeight(140)

        self.snooze_enabled = QCheckBox("Wiedervorlage festlegen")

        self.snooze_date = QDateEdit()
        self.snooze_date.setCalendarPopup(True)
        self.snooze_date.setDate(QDate.currentDate())
        self.snooze_date.setEnabled(False)

        if self.idea.snoozed_until is not None:
            self.snooze_enabled.setChecked(True)
            self.snooze_date.setEnabled(True)

            self.snooze_date.setDate(
                QDate(
                    self.idea.snoozed_until.year,
                    self.idea.snoozed_until.month,
                    self.idea.snoozed_until.day,
                )
            )

        self.snooze_enabled.toggled.connect(
            self.snooze_date.setEnabled
        )

        convert_button = QPushButton("Als Task definieren")
        discard_button = QPushButton("Verwerfen")

        convert_button.clicked.connect(
            self.request_conversion
        )

        discard_button.clicked.connect(
            self.discard_idea
        )

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(self.save_idea)
        buttons.rejected.connect(self.reject)

        layout.addWidget(thought_label)
        layout.addWidget(self.thought_input)
        layout.addWidget(self.snooze_enabled)
        layout.addWidget(self.snooze_date)
        layout.addSpacing(12)
        layout.addWidget(convert_button)
        layout.addWidget(discard_button)
        layout.addWidget(buttons)

    def save_idea(self):
        thought = self.thought_input.toPlainText().strip()

        if not thought:
            return

        self.idea.thought = thought

        if self.snooze_enabled.isChecked():
            selected_date = self.snooze_date.date()

            self.idea.snoozed_until = selected_date.toPython()
            self.idea.status = IdeaNoteStatus.SNOOZED
        else:
            self.idea.snoozed_until = None
            self.idea.status = IdeaNoteStatus.INBOX

        self.action = "saved"
        self.accept()

    def request_conversion(self):
        thought = self.thought_input.toPlainText().strip()

        if not thought:
            return

        self.idea.thought = thought
        self.action = "convert"

        self.accept()

    def discard_idea(self):
        self.idea.status = IdeaNoteStatus.DISCARDED
        self.action = "discard"

        self.accept()