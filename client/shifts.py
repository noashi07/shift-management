import json
import socket
import threading
from PyQt6.QtCore import Qt, pyqtSignal, QObject
from PyQt6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QLabel


class SignalEmitter(QObject):
    table_updated = pyqtSignal(list)


class Shifts(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.host = parent.host
        self.port = parent.tcp_port
        self.socket = None
        self.running = False
        self.signals = SignalEmitter()

        self.table_widget = QTableWidget(self)
        self.table_widget.setRowCount(7)
        self.table_widget.setColumnCount(7)

        self.table_widget.setHorizontalHeaderLabels(
            ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
        self.table_widget.setVerticalHeaderLabels(["07:00", "07:00", "07:00", "12:00", "16:00", "16:00", "17:00"])

        # Initialize table with empty data
        for row in range(7):
            for col in range(7):
                self.table_widget.setItem(row, col, QTableWidgetItem(""))

        self.table_widget.setStyleSheet("""
            QTableWidget {
                background-color: lightgray;
                border: 1px solid black;
            }
            QTableWidget::item {
                padding: 5px;
                color: black;
            }
            QHeaderView::section {
                background-color: gray;
                color: black;
                padding: 5px;
            }
        """)

        title_label = QLabel("WORK", self)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(self.table_widget, stretch=1)
        self.setLayout(layout)

        # Connect signals and slots
        self.table_widget.itemChanged.connect(self.send_table_update)
        self.signals.table_updated.connect(self.update_table_from_server)

        # Start TCP connection
        self.connect_to_server()

    def connect_to_server(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.running = True
            threading.Thread(target=self.listen_to_server, daemon=True).start()
        except Exception as e:
            print(f"Failed to connect to server: {e}")

    def listen_to_server(self):
        while self.running:
            try:
                data = self.socket.recv(1024).decode()
                if data:
                    message = json.loads(data)
                    if message["type"] == "table_update":
                        self.signals.table_updated.emit(message["data"])
            except Exception as e:
                print(f"Error receiving data: {e}")
                self.running = False
                break

    def send_table_update(self, item):
        if not self.socket or not self.running:
            return

        row = item.row()
        col = item.column()
        value = item.text()

        message = json.dumps({
            "type": "update_table",
            "row": row,
            "col": col,
            "value": value
        })
        try:
            self.socket.sendall(message.encode())
        except Exception as e:
            print(f"Error sending update: {e}")

    def update_table_from_server(self, table_data):
        self.table_widget.blockSignals(True)  # Prevent recursive updates
        for row in range(7):
            for col in range(7):
                item = self.table_widget.item(row, col)
                if item is None:
                    item = QTableWidgetItem()
                    self.table_widget.setItem(row, col, item)
                item.setText(table_data[row][col])
        self.table_widget.blockSignals(False)

    def closeEvent(self, event):
        self.running = False
        if self.socket:
            self.socket.close()
        event.accept()
