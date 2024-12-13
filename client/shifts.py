from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit


class Shifts(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # קביעת כותרת החלון
        self.setWindowTitle("Client - Send Message")

        # הצגת החלון במצב מסך מלא
        self.showFullScreen()

        # קביעת צבע הרקע של החלון ללבן
        self.setStyleSheet("background-color: white;")

        self.user_name = QLineEdit(parent=self)
