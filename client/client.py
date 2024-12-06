from PyQt6.QtWidgets import QApplication, QGridLayout, QLabel, QLineEdit, QPushButton, QWidget
import socket


class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Client - Send Message")
        self.resize(300, 150)

        # יצירת סוקט (socket) חדש
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # הגדרת כתובת ה-IP והפורט של השרת שאליו הלקוח יתחבר
        self.host = '127.0.0.1'  # IP של השרת (localhost)
        self.port = 12345  # הפורט שבו השרת מאזין

        # התחברות לשרת
        try:
            self.client_socket.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")
        except ConnectionRefusedError:
            print("Connection failed. Server may not be running.")

        # יצירת שדות קלט (user_name, password)
        self.user_name = QLineEdit(parent=self)
        self.password = QLineEdit(parent=self)

        # יצירת כפתור לשליחת ההודעה
        action_button = QPushButton(parent=self, text="Send Message")

        # חיבור הכפתור לפונקציה שתשלח את ההודעה
        action_button.clicked.connect(self.send_message)

        # הגדרת פריסת התצוגה (Layout)
        layout = QGridLayout()
        layout.addWidget(self.user_name, 0, 0, 1, 2)  # שדה שם משתמש
        layout.addWidget(self.password, 1, 0, 1, 2)  # שדה סיסמה
        layout.addWidget(action_button, 2, 0, 1, 2)  # כפתור שליחה
        self.setLayout(layout)

    def send_message(self):
        # קבלת הטקסט מהשדות
        user_name_text = self.user_name.text()
        user_password_text = self.password.text()

        # אם יש טקסט בשני השדות, שלח את ההודעה
        if user_name_text and user_password_text:
            message = f"Username: {user_name_text}, Password: {user_password_text}"
            try:
                # שלח את ההודעה לשרת
                self.client_socket.send(message.encode('utf-8'))
                print(f"Sent to server: {message}")

                # קבל תשובה מהשרת
                response = self.client_socket.recv(1024).decode('utf-8')
                print(f"Received from server: {response}")

            except Exception as e:
                print(f"Error sending message: {e}")
        else:
            # אם אחד מהשדות ריק, הצג הודעה מתאימה בשדות
            if not user_name_text:
                self.user_name.setText("No username to send")
            if not user_password_text:
                self.password.setText("No password to send")


# הפעלת האפליקציה של PyQt
app = QApplication([])

# יצירת חלון הלקוח והצגתו
window = Window()
window.show()

# הפעלת לולאת האפליקציה
app.exec()