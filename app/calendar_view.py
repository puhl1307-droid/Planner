from datetime import date, timedelta

from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
)

from app.calendar_canvas import (
    CALENDAR_BOTTOM_PADDING,
    CALENDAR_END_HOUR,
    CALENDAR_LEFT_MARGIN,
    CALENDAR_RIGHT_MARGIN,
    CALENDAR_START_HOUR,
    CALENDAR_TOP_PADDING,
    HOUR_HEIGHT,
    CalendarCanvas,
)

from app.dialogs.work_block_dialog import (
    WorkBlockDialog,
)

from app.services.work_block_service import (
    WorkBlockService,
)


class CalendarView(QFrame):
    def __init__(self):
        super().__init__()

        self.work_block_service = (
            WorkBlockService()
        )

        self.current_date = date.today()

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            24,
            20,
            24,
            20,
        )

        layout.setSpacing(16)

        layout.addLayout(
            self.create_view_switch()
        )

        layout.addLayout(
            self.create_calendar_header()
        )

        self.scroll_area = QScrollArea()

        self.scroll_area.setWidgetResizable(
            True
        )

        self.scroll_area.setFrameShape(
            QFrame.Shape.NoFrame
        )

        self.calendar_container = (
            CalendarCanvas()
        )

        calendar_height = (
            (
                CALENDAR_END_HOUR
                - CALENDAR_START_HOUR
            )
            * HOUR_HEIGHT
            + CALENDAR_TOP_PADDING
            + CALENDAR_BOTTOM_PADDING
        )

        self.calendar_container.setMinimumHeight(
            calendar_height
        )

        self.scroll_area.setWidget(
            self.calendar_container
        )

        layout.addWidget(
            self.scroll_area
        )

    def create_view_switch(self):
        layout = QHBoxLayout()

        day_button = QPushButton("Tag")
        week_button = QPushButton("Woche")

        day_button.setFixedWidth(90)
        week_button.setFixedWidth(90)

        layout.addStretch()

        layout.addWidget(
            day_button
        )

        layout.addWidget(
            week_button
        )

        layout.addStretch()

        return layout

    def create_calendar_header(self):
        layout = QHBoxLayout()

        work_block_button = QPushButton(
            "+ WorkBlock"
        )

        previous_button = QPushButton("←")
        next_button = QPushButton("→")

        self.date_label = QLabel(
            self.current_date.strftime("%d.%m.%Y")
        )

        self.date_label.setStyleSheet(
            "font-size: 20px;"
            "font-weight: 600;"
        )

        previous_button.setFixedWidth(40)
        next_button.setFixedWidth(40)

        layout.addWidget(
            self.date_label
        )

        layout.addStretch()

        layout.addWidget(
            work_block_button
        )

        work_block_button.clicked.connect(
            self.open_work_block_dialog
        )

        layout.addWidget(
            previous_button
        )

        layout.addWidget(
            next_button
        )

        previous_button.clicked.connect(
            self.show_previous_day
        )

        next_button.clicked.connect(
            self.show_next_day
        )

        return layout

    def minutes_from_calendar_start(
        self,
        hour,
        minute,
    ):
        return (
            (
                hour
                - CALENDAR_START_HOUR
            )
            * 60
            + minute
        )

    def minutes_to_pixels(
        self,
        minutes,
    ):
        return (
            minutes
            / 60
            * HOUR_HEIGHT
        )

    def open_work_block_dialog(self):
        dialog = WorkBlockDialog(
            parent=self
        )

        if (
            dialog.exec()
            != QDialog.DialogCode.Accepted
        ):
            return

        title = (
            dialog.title_input
            .text()
            .strip()
        )

        if not title:
            return

        start_at = (
            dialog.start_input
            .dateTime()
            .toPython()
        )

        end_at = (
            dialog.end_input
            .dateTime()
            .toPython()
        )

        description = (
            dialog.description_input
            .toPlainText()
            .strip()
            or None
        )

        self.work_block_service.create_work_block(
            title=title,
            start_at=start_at,
            end_at=end_at,
            focus_level=(
                dialog.focus_input
                .currentData()
            ),
            description=description,
        )

        self.render_calendar_items()

    def add_work_block_widget(
        self,
        work_block,
    ):
        if (
            work_block.start_at.date()
            != self.current_date
        ):
            return

        start_minutes = (
            work_block.start_at.hour
            * 60
            + work_block.start_at.minute
        )

        calendar_start_minutes = (
            CALENDAR_START_HOUR
            * 60
        )

        minutes_from_start = (
            start_minutes
            - calendar_start_minutes
        )

        duration_minutes = int(
            (
                work_block.end_at
                - work_block.start_at
            ).total_seconds()
            / 60
        )

        y_position = (
            CALENDAR_TOP_PADDING
            + int(
                self.minutes_to_pixels(
                    minutes_from_start
                )
            )
        )

        block_height = int(
            self.minutes_to_pixels(
                duration_minutes
            )
        )

        block = QFrame(
            self.calendar_container
        )

        block.setObjectName(
            "workBlock"
        )

        block.setStyleSheet(
            """
            QFrame {
                background-color: #f0f0f0;
                border: 1px solid #bdbdbd;
                border-radius: 6px;
            }
            """
        )

        layout = QVBoxLayout(block)

        layout.setContentsMargins(
            8,
            6,
            8,
            6,
        )

        title_label = QLabel(
            work_block.title
        )

        focus_label = QLabel(
            "Fokus: "
            f"{work_block.focus_level.value}"
        )

        layout.addWidget(
            title_label
        )

        layout.addWidget(
            focus_label
        )

        block_width = max(
            0,
            (
                self.calendar_container.width()
                - CALENDAR_LEFT_MARGIN
                - CALENDAR_RIGHT_MARGIN
            ),
        )

        block.setGeometry(
            CALENDAR_LEFT_MARGIN,
            y_position,
            block_width,
            block_height,
        )

        block.show()
        block.raise_()

    def render_calendar_items(self):
        existing_work_blocks = (
            self.calendar_container
            .findChildren(
                QFrame,
                "workBlock",
            )
        )

        for widget in existing_work_blocks:
            widget.deleteLater()

        for work_block in (
            self.work_block_service
            .work_blocks
        ):
            if (
                work_block.start_at.date()
                == self.current_date
            ):
                self.add_work_block_widget(
                    work_block
                )

    def resizeEvent(self, event):
        super().resizeEvent(event)

        if hasattr(
            self,
            "calendar_container",
        ):
            self.render_calendar_items()


    def show_previous_day(self):
        self.current_date -= timedelta(days=1)
        self.update_current_date()


    def show_next_day(self):
        self.current_date += timedelta(days=1)
        self.update_current_date()


    def update_current_date(self):
        self.date_label.setText(
            self.current_date.strftime("%d.%m.%Y")
        )

        self.render_calendar_items()