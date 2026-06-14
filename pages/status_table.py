from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class StatusTable(QTableWidget):
    def __init__(self):
        super().__init__(0, 4)
        self.setup_ui()

    def setup_ui(self):
        self.setHorizontalHeaderLabels([
            "Device Name",
            "IP Address",
            "Type",
            "Status"
        ])
        self.verticalHeader().setVisible(False)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.horizontalHeader().setStretchLastSection(True)

        self.setStyleSheet("""
            QTableWidget {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 10px;
                padding: 8px;
                font-family: Arial;
            }
            QHeaderView::section {
                background-color: #007bff;
                color: white;
                padding: 8px;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)

        self.setColumnWidth(0, 220)
        self.setColumnWidth(1, 180)
        self.setColumnWidth(2, 140)
        self.setColumnWidth(3, 120)

        sample_devices = [
            {"name": "Switch 1", "ip": "192.168.1.10", "type": "Switch", "status": "Online"},
            {"name": "Router 1", "ip": "192.168.1.20", "type": "Router", "status": "Online"},
            {"name": "Access Point", "ip": "192.168.1.30", "type": "Access Point", "status": "Offline"},
            {"name": "Firewall", "ip": "192.168.1.40", "type": "Firewall", "status": "Online"},
        ]
        self.update_table(sample_devices)

    def update_table(self, devices):
        self.setRowCount(len(devices))
        for row, device in enumerate(devices):
            name_item = QTableWidgetItem(device["name"])
            ip_item = QTableWidgetItem(device["ip"])
            type_item = QTableWidgetItem(device["type"])
            status_item = QTableWidgetItem(device["status"])

            for item in [name_item, ip_item, type_item, status_item]:
                item.setFont(QFont("Arial", 11))
                item.setTextAlignment(Qt.AlignCenter)

            if device["status"] == "Online":
                status_item.setForeground(Qt.darkGreen)
            else:
                status_item.setForeground(Qt.red)

            self.setItem(row, 0, name_item)
            self.setItem(row, 1, ip_item)
            self.setItem(row, 2, type_item)
            self.setItem(row, 3, status_item)
