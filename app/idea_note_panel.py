from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from app.models.idea_note import IdeaNote, IdeaNoteStatus
from app.dialogs.idea_note_dialog import IdeaNoteDialog


class IdeaNotePanel(QFrame):
    idea_created = Signal(IdeaNote)
    idea_conversion_requested = Signal(object, object)

    def __init__(self, ideas: list[IdeaNote] | None = None):
        super().__init__()

        self.ideas = ideas or []

        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(8)

        title = QLabel("Inbox")

        self.input = QLineEdit()
        self.input.setPlaceholderText("Idee / Notiz erfassen ...")
        self.input.returnPressed.connect(self.create_idea)

        self.layout.addWidget(title)
        self.layout.addWidget(self.input)

        for idea in self.ideas:
            self.add_idea_widget(idea)

    def create_idea(self):
        thought = self.input.text().strip()

        if not thought:
            return

        idea = IdeaNote(
            id=self.next_idea_id(),
            thought=thought,
        )

        self.ideas.append(idea)
        self.add_idea_widget(idea)

        self.input.clear()

        self.idea_created.emit(idea)


    def add_idea_widget(self, idea):
        frame = QFrame()

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)

        idea_button = QPushButton(idea.thought)
        idea_button.setToolTip("Idee öffnen")

        idea_button.clicked.connect(
            lambda: self.open_idea_dialog(
                idea,
                frame,
                idea_button,
            )
        )

        layout.addWidget(idea_button)

        self.layout.addWidget(frame)


    def open_idea_dialog(
        self,
        idea,
        frame,
        idea_button,
    ):
        dialog = IdeaNoteDialog(
            idea=idea,
            parent=self,
        )

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        if dialog.action == "saved":
            if idea.status == IdeaNoteStatus.SNOOZED:
                frame.hide()
                return

            idea_button.setText(idea.thought)

        elif dialog.action == "discard":
            frame.hide()

        elif dialog.action == "convert":
            self.idea_conversion_requested.emit(
                idea,
                frame,
            )


    def next_idea_id(self):
        if not self.ideas:
            return 1

        return max(
            idea.id for idea in self.ideas
        ) + 1