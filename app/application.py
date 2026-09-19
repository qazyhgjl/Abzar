from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from ui.main_window import MainWindow


def run():
    app = QApplication([])
    app.setApplicationName("شبیه‌ساز حرکت انسان آفلاین")
    app.setLayoutDirection(Qt.RightToLeft)
    window = MainWindow()
    window.show()
    return app.exec()
