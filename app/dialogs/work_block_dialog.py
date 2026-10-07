from PySide6.QtCore import QDateTime
from PySide6.QtWidgets import (
    QComboBox,
    QDateTimeEdit,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QPlainTextEdit,
    QVBoxLayout,
)

from app.models.focus_level import FocusLevel


class WorkBlockDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("WorkBlock erstellen")
        self.setMinimumWidth(450)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.title_input = QLineEdit()

        self.start_input = QDateTimeEdit()
        self.start_input.setCalendarPopup(True)
        self.start_input.setDisplayFormat("dd.MM.yyyy HH:mm")

        self.end_input = QDateTimeEdit()
        self.end_input.setCalendarPopup(True)
        self.end_input.setDisplayFormat("dd.MM.yyyy HH:mm")

        now = QDateTime.currentDateTime()

        self.start_input.setDateTime(now)
        self.end_input.setDateTime(now.addSecs(60 * 60))

        self.focus_input = QComboBox()
        self.focus_input.addItem("Niedrig", FocusLevel.LOW)
        self.focus_input.addItem("Mittel", FocusLevel.MEDIUM)
        self.focus_input.addItem("Hoch", FocusLevel.HIGH)

        self.description_input = QPlainTextEdit()
        self.description_input.setMaximumHeight(100)

        form.addRow("Titel:", self.title_input)
        form.addRow("Start:", self.start_input)
        form.addRow("Ende:", self.end_input)
        form.addRow("Fokuslevel:", self.focus_input)
        form.addRow("Beschreibung:", self.description_input)

        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(self.validate_and_accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)


    def validate_and_accept(self):
        title = self.title_input.text().strip()

        if not title:
            QMessageBox.warning(
                self,
                "Ungültige Eingabe",
                "Bitte gib einen Titel für den WorkBlock ein.",
            )
            return

        start_at = self.start_input.dateTime().toPython()
        end_at = self.end_input.dateTime().toPython()

        if end_at <= start_at:
            QMessageBox.warning(
                self,
                "Ungültige Eingabe",
                "Das Ende muss nach dem Beginn liegen.",
            )
            return

        if start_at.date() != end_at.date():
            QMessageBox.warning(
                self,
                "Ungültige Eingabe",
                "Ein WorkBlock muss innerhalb eines Tages liegen.",
            )
            return

        self.accept()