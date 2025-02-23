from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QLabel


class Shifts(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)


        # יצירת טבלה
        self.table_widget = QTableWidget(self)

        # קביעת מספר השורות והעמודות בטבלה
        self.table_widget.setRowCount(5)  # 5 שורות
        self.table_widget.setColumnCount(8)  # 7 עמודות

        # קביעת שמות העמודות
        self.table_widget.setHorizontalHeaderLabels(["Time","Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"])


        # הוספת נתונים לטבלה
        data = [
            ("07:00", " ", " ", " ", " ", " ", " ",""),
            ("07:00", " ", " ", " ", " ", " ", " ",""),
            ("07:00", " ", " ", " ", " ", " ", " ",""),
            ("12:00", " ", " ", " ", " ", " ", " ",""),
            ("16:00", " ", " ", " ", " ", " ", " ", ""),
            ("16:00", " ", " ", " ", " ", " ", " ", ""),
            ("16:00", " ", " ", " ", " ", " ", " ", ""),
        ]
        for row, (time, sunday, monday, tuesday, wednesday, thursday, friday, saturday) in enumerate(data):
            self.table_widget.setItem(row, 0, QTableWidgetItem(time))
            self.table_widget.setItem(row, 1, QTableWidgetItem(sunday))
            self.table_widget.setItem(row, 2, QTableWidgetItem(monday))
            self.table_widget.setItem(row, 3, QTableWidgetItem(tuesday))
            self.table_widget.setItem(row, 4, QTableWidgetItem(wednesday))
            self.table_widget.setItem(row, 5, QTableWidgetItem(thursday))
            self.table_widget.setItem(row, 6, QTableWidgetItem(friday))
            self.table_widget.setItem(row, 7, QTableWidgetItem(saturday))


        # עיצוב הטבלה עם רקע אפור
        self.table_widget.setStyleSheet("""
             QTableWidget {
                 background-color: lightgray;  /* Gray background */
                 border: 1px solid black;
             }
             QTableWidget::item {
                 padding: 5px;
                 color: black;
             }
             QHeaderView::section {
                 background-color: gray;
                 color: black;  /* Header text in black */
                 padding: 5px;
             }
         """)

        # יצירת כותרת בחלק העליון של החלון
        title_label = QLabel("WORK", self)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # יצירת פריסת Layout
        layout = QVBoxLayout()

        # הוספת הכותרת לפריסת ה-Layout
        layout.addWidget(title_label)

        # הוספת הטבלה כך שהיא תתפוס את כל השטח הפנוי
        layout.addWidget(self.table_widget, stretch=1)  # stretch=1 גורם לטבלה לתפוס את כל השטח הפנוי

        # קביעת ה-Layout של החלון
        self.setLayout(layout)
