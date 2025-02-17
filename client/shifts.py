from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QLabel


class Shifts(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)


        # יצירת טבלה
        self.table_widget = QTableWidget(self)

        # קביעת מספר השורות והעמודות בטבלה
        self.table_widget.setRowCount(5)  # 5 שורות
        self.table_widget.setColumnCount(3)  # 3 עמודות

        # קביעת שמות העמודות
        self.table_widget.setHorizontalHeaderLabels(["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"])

        # הוספת נתונים לטבלה
        data = [
            ("", " ", ""),
            ("", " ", ""),
            ("", " ", ""),
            ("", " ", ""),
            ("", " ", ""),
        ]

        for row, (sunday, monday, tuesday, wednesday, thursday, friday, saturday) in enumerate(data):
            self.table_widget.setItem(row, 0, QTableWidgetItem(sunday))  # Sunday column (index 0)
            self.table_widget.setItem(row, 1, QTableWidgetItem(monday))  # Monday column (index 1)
            self.table_widget.setItem(row, 2, QTableWidgetItem(tuesday))  # Tuesday column (index 2)
            self.table_widget.setItem(row, 3, QTableWidgetItem(wednesday))  # Wednesday column (index 3)
            self.table_widget.setItem(row, 4, QTableWidgetItem(thursday))  # Thursday column (index 4)
            self.table_widget.setItem(row, 5, QTableWidgetItem(friday))  # Friday column (index 5)
            self.table_widget.setItem(row, 6, QTableWidgetItem(saturday))  # Saturday column (index 6)

        # עיצוב הטבלה עם רקע אפור
        self.table_widget.setStyleSheet("""
             QTableWidget {
                 background-color: lightgray;  /* Gray background */
                 border: 1px solid black;
             }
             QTableWidget::item {
                 padding: 5px;
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
