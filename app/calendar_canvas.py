from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QWidget


CALENDAR_START_HOUR = 6
CALENDAR_END_HOUR = 23

HOUR_HEIGHT = 80
GRID_MINUTES = 15

CALENDAR_TOP_PADDING = 16
CALENDAR_BOTTOM_PADDING = 16

CALENDAR_LEFT_MARGIN = 70
CALENDAR_RIGHT_MARGIN = 20


class CalendarCanvas(QWidget):
    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)

        total_minutes = (
            CALENDAR_END_HOUR - CALENDAR_START_HOUR
        ) * 60

        line_end = (
            self.width()
            - CALENDAR_RIGHT_MARGIN
        )

        for minutes in range(
            0,
            total_minutes + 1,
            GRID_MINUTES,
        ):
            y_position = (
                CALENDAR_TOP_PADDING
                + int(
                    minutes / 60
                    * HOUR_HEIGHT
                )
            )

            absolute_minutes = (
                CALENDAR_START_HOUR * 60
                + minutes
            )

            hour = (
                absolute_minutes // 60
            )

            minute = (
                absolute_minutes % 60
            )

            if minute == 0:
                line_color = QColor(
                    "#b0b0b0"
                )

            elif minute == 30:
                line_color = QColor(
                    "#d0d0d0"
                )

            else:
                line_color = QColor(
                    "#e8e8e8"
                )

            painter.setPen(
                QPen(
                    line_color,
                    1,
                )
            )

            painter.drawLine(
                CALENDAR_LEFT_MARGIN,
                y_position,
                line_end,
                y_position,
            )

            if minute == 0:
                painter.setPen(
                    QColor("#555555")
                )

                painter.drawText(
                    0,
                    y_position - 10,
                    55,
                    20,
                    0,
                    f"{hour:02d}:00",
                )