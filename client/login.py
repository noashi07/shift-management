import json
import requests
from PyQt6.QtWidgets import QGridLayout, QLabel, QLineEdit, QPushButton, QWidget
import tkinter as tk
from tkinter import messagebox


class Login(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login Page")
        self.resize(300, 150)

        self.main_stack = parent

        self.user_name_label = QLabel("שם משתמש:")
        self.user_name = QLineEdit(parent=self)

        self.password_label = QLabel("סיסמה:")
        self.password = QLineEdit(parent=self)
        self.password.setEchoMode(QLineEdit.EchoMode.Password)  # Hide password input

        action_button = QPushButton(parent=self, text="Send Message")
        action_button.clicked.connect(self.send_message)

        layout = QGridLayout()
        layout.addWidget(self.user_name_label, 0, 0, 1, 2)
        layout.addWidget(self.user_name, 1, 0, 1, 2)
        layout.addWidget(self.password_label, 2, 0, 1, 2)
        layout.addWidget(self.password, 3, 0, 1, 2)
        layout.addWidget(action_button, 4, 0, 1, 2)
        self.setLayout(layout)

    def send_message(self):
        user_name_text = self.user_name.text().strip()
        user_password_text = self.password.text().strip()

        if user_name_text and user_password_text:
            try:
                headers = {'Content-Type': 'application/json'}  # Add proper headers
                payload = json.dumps({'username': user_name_text, 'password': user_password_text})
                response = requests.post(
                    f'http://{self.main_stack.host}:{self.main_stack.http_port}/user/login',
                    data=payload,
                    headers=headers
                )

                response.raise_for_status()  # Raise exception for bad status codes
                data = response.json()

                if 'error' in data:
                    show_error_message(data.get('reason', 'Unknown error occurred'))
                else:
                    self.main_stack.stacked.setCurrentWidget(self.main_stack.stacked.widget(1))
            except requests.exceptions.RequestException as e:
                show_error_message(f"Connection error: {str(e)}")
        else:
            if not user_name_text:
                self.user_name.setText("No username to send")
            if not user_password_text:
                self.password.setText("No password to send")


def show_error_message(error_message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Login Error", error_message)
    root.destroy()  # Properly close the Tk instance
