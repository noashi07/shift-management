import sys
from PyQt6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QApplication

from login import Login
from shifts import Shifts
from register import Register


class MainStack(QWidget):
    def __init__(self, *args, **kwargs):
        super(MainStack, self).__init__(*args, **kwargs)

        self.host = 'localhost'
        self.http_port = 8080  # Match server.py HTTP port
        self.tcp_port = 8081  # Match server.py TCP port

        login_widget = Login(self)
        shifts_widget = Shifts(self)
        register_widget = Register(self)

        self.stacked = QStackedWidget(self)
        self.stacked.addWidget(login_widget)
        self.stacked.addWidget(shifts_widget)
        self.stacked.addWidget(register_widget)

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
