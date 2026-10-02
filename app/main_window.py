from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Planner")
        self.resize(1400, 900)

        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        sidebar = self.create_sidebar()
        calendar = self.create_calendar_area()
        task_panel = self.create_task_panel()

        main_layout.addWidget(sidebar, 1)
        main_layout.addWidget(calendar, 4)
        main_layout.addWidget(task_panel, 2)

    def create_sidebar(self):
        frame = QFrame()

        layout = QVBoxLayout(frame)

        title = QLabel("Planner")
        today = QLabel("Heute")
        week = QLabel("Woche")
        tasks = QLabel("Aufgaben")
        projects = QLabel("Projekte")

        layout.addWidget(title)
        layout.addSpacing(20)

        layout.addWidget(today)
        layout.addWidget(week)
        layout.addWidget(tasks)
        layout.addWidget(projects)

        layout.addStretch()

        return frame

    def create_calendar_area(self):
        frame = QFrame()

        layout = QVBoxLayout(frame)

        title = QLabel("Heute")
        placeholder = QLabel("Hier entsteht später das Time Grid")

        layout.addWidget(title)
        layout.addWidget(placeholder)
        layout.addStretch()

        return frame

    def create_task_panel(self):
        frame = QFrame()

        layout = QVBoxLayout(frame)

        title = QLabel("Offene Aufgaben")

        layout.addWidget(title)
        layout.addWidget(QLabel("☐ Beispielaufgabe 1"))
        layout.addWidget(QLabel("☐ Beispielaufgabe 2"))
        layout.addWidget(QLabel("☐ Beispielaufgabe 3"))

        layout.addStretch()

        return frame