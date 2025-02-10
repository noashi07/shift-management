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
        # קבלת הטקסט מהשדות
        user_name_text = self.user_name.text()
        user_password_text = self.password.text()

        # אם יש טקסט בשני השדות, שלח את ההודעה
        if user_name_text and user_password_text:
            x = requests.post('http://localhost:8080/user/login',
                              data=json.dumps({'username': user_name_text, 'password': user_password_text}))
            response = x.json()
            if 'error' in response:
                error_message = response.get('reason', 'Unknown error occurred')
                show_error_message(error_message)
            else:
                pass

        else:
            # אם אחד מהשדות ריק, הצג הודעה מתאימה בשדות
            if not user_name_text:
                self.user_name.setText("No username to send")
            if not user_password_text:
                self.password.setText("No password to send")


def show_error_message(error_message):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showerror("Login Error", error_message)
    root.quit()
