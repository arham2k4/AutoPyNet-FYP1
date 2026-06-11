from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QPushButton,
                            QLabel, QTableWidget, QTableWidgetItem, QWidget, QLineEdit)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import importlib
import socket

class SingleDevicePage(QFrame):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.current_vendor = None
        self.current_device_type = "switch"
        self.command_buttons = []
        self.init_ui()

    def set_selected_options(self, vendor, device_type):
        self.current_vendor = vendor
        self.current_device_type = device_type
        self.load_commands()

    def load_commands(self):
        if self.current_device_type == "switch":
            self.load_switch_commands()
        elif self.current_device_type == "router":
            self.load_router_commands()

    def init_ui(self):
        content_layout = QVBoxLayout()

        device_selection_frame = QFrame()
        container_layout = QVBoxLayout()
        device_selection_frame.setLayout(container_layout)
        device_selection_frame.setFixedSize(1680, 970)
        device_selection_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 20px;
                border: 2px solid #dcdcdc;
            }
        """)

        title_label = QLabel("Single Device")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("margin: 20px 0; font-weight: bold;")
        container_layout.addWidget(title_label)

        device_type_layout = QHBoxLayout()
        device_type_layout.setSpacing(0)

        self.switch_button = QPushButton("Switch")
        self.router_button = QPushButton("Router")

        for btn in [self.switch_button, self.router_button]:
            btn.setFixedHeight(40)
            btn.setFont(QFont("Arial", 12))

        self.switch_button.clicked.connect(lambda: self.set_active_device_type("switch"))
        self.router_button.clicked.connect(lambda: self.set_active_device_type("router"))

        device_type_layout.addWidget(self.switch_button)
        device_type_layout.addWidget(self.router_button)
        device_type_layout.addStretch()
        container_layout.addLayout(device_type_layout)

        # IP Address Input
        ip_input_layout = QHBoxLayout()
        ip_input_layout.setContentsMargins(20, 10, 20, 20)
        
        ip_label = QLabel("IP Address:")
        ip_label.setFont(QFont("Arial", 12))
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Enter device IP address...")
        self.ip_input.setFixedHeight(40)
        self.ip_input.setFont(QFont("Arial", 12))
        self.ip_input.setStyleSheet("""
            QLineEdit {
                # border: 2px solid #dcdcdc;
                # border-radius: 8px;
                padding: 0 10px;
            }
            QLineEdit:focus {
                # border-color: #4CAF50;
            }
        """)

        self.ip_input.textChanged.connect(self.check_ip_and_toggle_buttons)

        ip_input_layout.addWidget(ip_label)
        ip_input_layout.addWidget(self.ip_input)
        ip_input_layout.addStretch()
        container_layout.addLayout(ip_input_layout)
        ip_label = QLabel("IP Address:")
        ip_label.setFont(QFont("Arial", 12))
        ip_label.setStyleSheet("border: none;")  # <- Remove border explicitly


        # Command Table
        self.single_device_table = QTableWidget()
        self.single_device_table.setColumnCount(1)
        self.single_device_table.setHorizontalHeaderLabels(["Code ID and Description"])
        self.single_device_table.setColumnWidth(0, 1650)
        self.single_device_table.verticalHeader().setVisible(False)
        self.single_device_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.single_device_table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.single_device_table.setStyleSheet("""
            QTableWidget {
                background-color: #f9f9f9;
                border: none;
                font-size: 12pt;
                gridline-color: #dcdcdc;
            }
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                border: none;
                padding: 8px;
            }
        """)

        container_layout.addWidget(self.single_device_table)

        # Back Button
        back_button = QPushButton("Back")
        back_button.setFixedSize(100, 40)
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border-radius: 8px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        back_button.clicked.connect(self.parent.open_device_selection_page)

        back_button_layout = QHBoxLayout()
        back_button_layout.addWidget(back_button)
        back_button_layout.setAlignment(Qt.AlignLeft)
        container_layout.addLayout(back_button_layout)

        content_layout.addWidget(device_selection_frame, alignment=Qt.AlignCenter)
        self.setLayout(content_layout)

        self.set_active_device_type("switch")

    def set_active_device_type(self, device_type):
        self.current_device_type = device_type
        self.parent.selected_device_type = device_type

        if device_type == "switch":
            self.switch_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    font-weight: bold;
                    border: none;
                    padding: 8px 20px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            self.router_button.setStyleSheet("""
                QPushButton {
                    background-color: #6c757d;
                    color: white;
                    border: none;
                    padding: 8px 20px;
                }
                QPushButton:hover {
                    background-color: #5a6268;
                }
            """)
        else:
            self.router_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    font-weight: bold;
                    border: none;
                    padding: 8px 20px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            self.switch_button.setStyleSheet("""
                QPushButton {
                    background-color: #6c757d;
                    color: white;
                    border: none;
                    padding: 8px 20px;
                }
                QPushButton:hover {
                    background-color: #5a6268;
                }
            """)

        self.load_commands()

    def load_switch_commands(self):
        commands = [
            ("0001", "show_running_config"),
            ("0002", "show_arp_table"),
            ("0003", "show_mac_address_table"),
            ("0004", "show_vlan_brief"),
            ("0005", "configure_vlan"),
        ]
        self.populate_command_table(commands)

    def load_router_commands(self):
        commands = [
            ("1001", "configure_rip"),
            ("1002", "enable_ip_routing"),
            ("1003", "set_hostname"),
            ("1004", "show_ip_interface_brief"),
            ("1005", "show_running_config")
        ]
        self.populate_command_table(commands)

    def populate_command_table(self, commands):
        self.single_device_table.clearContents()
        self.single_device_table.setRowCount(len(commands))
        self.command_buttons = []

        for row, (code_id, description) in enumerate(commands):
            button = QPushButton(f"{code_id} - {description}")
            button.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 10px;
                    font-size: 12pt;
                    background-color: #f0f0f0;
                    border: 1px solid #dcdcdc;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
            """)
            button.setEnabled(False)
            button.code_id = code_id
            button.description = description
            button.clicked.connect(lambda checked, b=button: self.handle_button_click(b))
            self.command_buttons.append(button)

            widget = QWidget()
            layout = QHBoxLayout(widget)
            layout.addWidget(button)
            layout.setContentsMargins(0, 0, 0, 0)

            self.single_device_table.setCellWidget(row, 0, widget)
            self.single_device_table.setRowHeight(row, 50)

        self.check_ip_and_toggle_buttons()

    def check_ip_and_toggle_buttons(self):
        ip = self.ip_input.text().strip()
        ip_valid = self.is_valid_ip(ip)

        for button in self.command_buttons:
            button.setEnabled(ip_valid)
            if not ip_valid:
                button.setStyleSheet("""
                    QPushButton {
                        text-align: left;
                        padding: 10px;
                        font-size: 12pt;
                        background-color: #f0f0f0;
                        border: 1px solid #dcdcdc;
                        border-radius: 5px;
                    }
                    QPushButton:hover {
                        background-color: #e0e0e0;
                    }
                """)

    def is_valid_ip(self, ip):
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False

    def handle_button_click(self, button):
        ip_address = self.ip_input.text()
        vendor = self.current_vendor
        device_type = self.current_device_type
        
        print("\n--- Selection Path ---")
        print(f"IP Address: {ip_address}")
        print(f"Vendor: {self.current_vendor}")
        print(f"Device Type: {self.current_device_type}")
        print(f"Configuration: {self.parent.selected_configuration}")
        print(f"Selected Code: {button.code_id} - {button.description}")
        print("----------------------\n")

        try:
            folder = f"{device_type.lower()}_single_device"
            module_path = f"Command.{vendor}.{device_type}.{folder}.{button.description}"
            print(f"Trying to import: {module_path}")
            script_module = importlib.import_module(module_path)

            if hasattr(script_module, "main"):
                script_module.main()
            else:
                print(f"'main' not found in {module_path}")
        except Exception as e:
            print(f"Import failed: {e}")

        # Reset button styles
        for row in range(self.single_device_table.rowCount()):
            widget = self.single_device_table.cellWidget(row, 0)
            if widget:
                btn = widget.findChild(QPushButton)
                if btn:
                    btn.setStyleSheet("""
                        QPushButton {
                            text-align: left;
                            padding: 10px;
                            font-size: 12pt;
                            background-color: #f0f0f0;
                            border: 1px solid #dcdcdc;
                            border-radius: 5px;
                        }
                        QPushButton:hover {
                            background-color: #e0e0e0;
                        }
                    """)

        # Highlight clicked button
        button.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 10px;
                font-size: 12pt;
                background-color: #0056b3;
                color: white;
                border: 1px solid #003d7a;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #004494;
            }
        """)

        # Clear IP input field after selection
        self.ip_input.clear()

        self.parent.open_main_page()

    def get_script_import_path(self, script_name: str) -> str:
        vendor = self.current_vendor
        device_type = self.current_device_type
        folder = f"{device_type.lower()}_single_device"

        if not vendor or not device_type:
            raise ValueError("Vendor and device type must be set.")

        return f"Command.{vendor}.{device_type}.{folder}.{script_name}"
