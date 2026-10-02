from datetime import date

from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

CALENDAR_START_HOUR = 6
CALENDAR_END_HOUR = 23

HOUR_HEIGHT = 80
GRID_MINUTES = 15

CALENDAR_TOP_PADDING = 16
CALENDAR_BOTTOM_PADDING = 16

class CalendarView(QFrame):
    def __init__(self):
        super().__init__()

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        layout.addLayout(self.create_view_switch())
        layout.addLayout(self.create_calendar_header())

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        calendar_container = QWidget()

        calendar_height = (
            CALENDAR_END_HOUR - CALENDAR_START_HOUR
        ) * HOUR_HEIGHT + CALENDAR_TOP_PADDING + CALENDAR_BOTTOM_PADDING

        calendar_container.setMinimumHeight(calendar_height)

        self.create_calendar_grid(calendar_container)

        planning_block = self.create_planning_block(
            title="Google Ads optimieren",
            start_hour=9,
            start_minute=0,
            duration_minutes=90,
        )

        planning_block.setParent(calendar_container)

        minutes_from_start = self.minutes_from_calendar_start(
            9,
            0,
        )

        y_position = CALENDAR_TOP_PADDING + int(
            self.minutes_to_pixels(minutes_from_start)
        )

        block_height = int(
            self.minutes_to_pixels(90)
        )

        planning_block.setGeometry(
            70,
            y_position,
            350,
            block_height,
        )

        planning_block.raise_()

        scroll_area.setWidget(calendar_container)
        layout.addWidget(scroll_area)

    def create_view_switch(self):
        layout = QHBoxLayout()

        day_button = QPushButton("Tag")
        week_button = QPushButton("Woche")

        day_button.setFixedWidth(90)
        week_button.setFixedWidth(90)

        layout.addStretch()
        layout.addWidget(day_button)
        layout.addWidget(week_button)
        layout.addStretch()

        return layout

    def create_calendar_header(self):
        layout = QHBoxLayout()

        previous_button = QPushButton("←")
        next_button = QPushButton("→")

        today = date.today()

        date_label = QLabel(
            today.strftime("%d.%m.%Y")
        )
        date_label.setStyleSheet(
            "font-size: 20px; font-weight: 600;"
        )

        previous_button.setFixedWidth(40)
        next_button.setFixedWidth(40)

        layout.addWidget(date_label)
        layout.addStretch()
        layout.addWidget(previous_button)
        layout.addWidget(next_button)

        return layout

    def create_grid_line(
        self,
        parent,
        hour,
        minute,
        y_position,
    ):
        time_label = QLabel(parent)
        time_label.setFixedWidth(55)

        if minute == 0:
            time_label.setText(
                f"{hour:02d}:00"
            )

        time_label.setGeometry(
            0,
            y_position - 10,
            55,
            20,
        )

        line = QFrame(parent)
        line.setFrameShape(QFrame.Shape.HLine)

        if minute == 0:
            line.setStyleSheet(
                "color: #b0b0b0;"
            )
        elif minute == 30:
            line.setStyleSheet(
                "color: #d0d0d0;"
            )
        else:
            line.setStyleSheet(
                "color: #e8e8e8;"
            )

        line.setGeometry(
            70,
            y_position,
            1000,
            1,
        )

    def create_planning_block(self, title, start_hour, start_minute, duration_minutes):
        block = QFrame()

        block.setStyleSheet("""
            QFrame {
                background-color: #e8eefc;
                border: 1px solid #b8c7f0;
                border-radius: 8px;
            }
        """)

        layout = QVBoxLayout(block)
        layout.setContentsMargins(10, 8, 10, 8)

        title_label = QLabel(title)

        time_label = QLabel(
            f"{start_hour:02d}:{start_minute:02d}"
        )

        layout.addWidget(title_label)
        layout.addWidget(time_label)
        layout.addStretch()

        return block

    def minutes_from_calendar_start(self, hour, minute):
        return (
            (hour - CALENDAR_START_HOUR) * 60
            + minute
        )

    def minutes_to_pixels(self, minutes):
        return (
            minutes / 60
            * HOUR_HEIGHT
        )

    def create_calendar_grid(self, parent):
        total_minutes = (
            CALENDAR_END_HOUR - CALENDAR_START_HOUR
        ) * 60

        for minutes in range(
            0,
            total_minutes + 1,
            GRID_MINUTES
        ):
            y_position = CALENDAR_TOP_PADDING + int(
                self.minutes_to_pixels(minutes)
            )

            absolute_minutes = (
                CALENDAR_START_HOUR * 60
                + minutes
            )

            hour = absolute_minutes // 60
            minute = absolute_minutes % 60

            self.create_grid_line(
                parent,
                hour,
                minute,
                y_position,
            )