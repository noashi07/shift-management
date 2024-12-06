from PyQt6.QtWidgets import QApplication, QWidget


class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # קביעת כותרת החלון
        self.setWindowTitle("Client - Send Message")

        # הצגת החלון במצב מסך מלא
        self.showFullScreen()

        # קביעת צבע הרקע של החלון ללבן
        self.setStyleSheet("background-color: white;")


# הפעלת אפליקציה
app = QApplication([])

# יצירת חלון והצגתו
window = Window()
window.show()

# הפעלת לולאת האפליקציה
app.exec()