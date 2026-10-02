from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
)


class TaskPanel(QFrame):
    def __init__(self):
        super().__init__()

        self.setFixedWidth(320)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title = QLabel("Tasks")
        title.setStyleSheet(
            "font-size: 18px; font-weight: 600;"
        )

        open_overview_button = QPushButton(
            "Tasks & Termine"
        )
        open_overview_button.setMinimumHeight(38)

        add_button = QPushButton("+ Task")
        add_button.setMinimumHeight(38)

        layout.addWidget(title)
        layout.addWidget(open_overview_button)
        layout.addWidget(add_button)
        layout.addSpacing(10)

        tasks = [
            "SEO-Text überarbeiten",
            "Rechnungen prüfen",
            "Newsletter vorbereiten",
        ]

        for task in tasks:
            task_label = QLabel(f"☐ {task}")
            task_label.setWordWrap(True)
            layout.addWidget(task_label)

        layout.addStretch()