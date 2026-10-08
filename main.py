import sys

from PySide6.QtWidgets import QApplication

from app.main_window import MainWindow
from app.styles.theme import apply_theme


app = QApplication(sys.argv)

apply_theme(app)

window = MainWindow()
window.show()

sys.exit(app.exec())