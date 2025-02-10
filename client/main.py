import sys
from PyQt6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QApplication
import socket
# QVBoxLayout-פריסת תצוגה בצורה אנכית(אחד מתחת לשני)
# QWidget- מחלקה בסיסית לאלמנטים גרפיים שמוצגים כמו: כפתור, תיבה ועוד.
# QApplication-מנהל את האירועים במערכת

from login import Login
from shifts import Shifts


class MainStack(QWidget):
    def __init__(self, *args, **kwargs):
        super(MainStack, self).__init__(*args, **kwargs)

        self.host = '127.0.0.1'
        self.port = 12345

        login_widget = Login()
        shifts_widget = Shifts()

        self.stacked = QStackedWidget(self)
        self.stacked.addWidget(login_widget)
        self.stacked.addWidget(shifts_widget)

        self.stacked.setCurrentWidget(login_widget)

        layout = QVBoxLayout(self)
        layout.addWidget(self.stacked)
        self.setLayout(layout)


def main():
    app = QApplication(sys.argv)
    main_stack = MainStack()
    main_stack.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
