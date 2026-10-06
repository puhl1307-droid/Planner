from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QWidget,
)

from app.calendar_view import CalendarView
from app.task_panel import TaskPanel
from app.sample_data import (
    create_sample_areas,
    create_sample_tasks,
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

        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        calendar_view = CalendarView()
        
        areas = create_sample_areas()
        tasks = create_sample_tasks()

        task_panel = TaskPanel(
            tasks=tasks,
            areas=areas,
        )

        layout.addWidget(calendar_view, 1)
        layout.addWidget(task_panel)