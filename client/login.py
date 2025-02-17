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

        # יצירת שדות קלט (user_name, password)
        self.user_name_label = QLabel("שם משתמש:")
        self.user_name = QLineEdit(parent=self)

        self.password_label = QLabel("סיסמה:")
        self.password = QLineEdit(parent=self)

        # יצירת כפתור לשליחת ההודעה
        action_button = QPushButton(parent=self, text="Send Message")
        # חיבור הכפתור לפונקציה שתשלח את ההודעה
        action_button.clicked.connect(self.send_message)

        # הגדרת פריסת התצוגה (Layout)
        layout = QGridLayout()
        layout.addWidget(self.user_name_label, 0, 0, 1, 2)  # שדה שם משתמש
        layout.addWidget(self.user_name, 1, 0, 1, 2)  # שדה שם משתמש
        layout.addWidget(self.password_label, 2, 0, 1, 2)  # שדה שם משתמש
        layout.addWidget(self.password, 3, 0, 1, 2)  # שדה סיסמה
        layout.addWidget(action_button, 4, 0, 1, 2)  # כפתור שליחה
        self.setLayout(layout)

    def send_message(self):
        # Get the text from the input fields
        user_name_text = self.user_name.text()
        user_password_text = self.password.text()

        # If both fields are filled, send the message
        if user_name_text and user_password_text:
            # Send the login request
            x = requests.post('http://localhost:8080/user/login',
                              data=json.dumps({'username': user_name_text, 'password': user_password_text}))
            response = x.json()

            if 'error' in response:
                # If there is an error, show an error message
                error_message = response.get('reason', 'Unknown error occurred')
                show_error_message(error_message)
            else:
                # If login is successful, switch to the shifts widget
                self.main_stack.stacked.setCurrentWidget(self.main_stack.stacked.widget(1))  # 1 refers to shifts_widget
        else:
            # If one of the fields is empty, set appropriate error text
            if not user_name_text:
                self.user_name.setText("No username to send")
            if not user_password_text:
                self.password.setText("No password to send")


def show_error_message(error_message):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showerror("Login Error", error_message)
    root.quit()
