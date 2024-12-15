import sys
from PyQt6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QApplication
import socket
#QVBoxLayout-פריסת תצוגה בצורה אנכית(אחד מתחת לשני)
#QWidget- מחלקה בסיסית לאלמנטים גרפיים שמוצגים כמו: כפתור, תיבה ועוד.
#QApplication-מנהל את האירועים במערכת

from login import Login
from shifts import Shifts


class MainStack(QWidget):
    def __init__(self, *args, **kwargs):
        super(MainStack, self).__init__(*args, **kwargs)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.host = '127.0.0.1'
        self.port = 12345

        try:
            self.client_socket.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")
        except ConnectionRefusedError:
            print("Connection failed. Server may not be running.")

        login_widget = Login(self.client_socket)
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
