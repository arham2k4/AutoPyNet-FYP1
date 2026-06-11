import importlib
import traceback
from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QTableWidget, QWidget, QMessageBox,
                             QFileDialog, QLineEdit)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class MultipleDevicePage(QFrame):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.current_device_type = "switch"
        self.current_vendor = None
        self.selected_file_path = None
        self.init_ui()

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

        title_label = QLabel("Multiple Devices")
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

        file_upload_layout = QHBoxLayout()
        file_upload_layout.setContentsMargins(20, 10, 20, 20)

        upload_button = QPushButton("Upload Your file Here")
        upload_button.setFixedHeight(40)
        upload_button.setFont(QFont("Arial", 12))
        upload_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 8px;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        upload_button.clicked.connect(self.handle_file_upload)

        self.file_path_display = QLineEdit()
        self.file_path_display.setPlaceholderText("No file selected...")
        self.file_path_display.setReadOnly(True)
        self.file_path_display.setFixedHeight(40)
        self.file_path_display.setFont(QFont("Arial", 12))
        self.file_path_display.setStyleSheet("""
            QLineEdit {
                border: 2px solid #dcdcdc;
                border-radius: 8px;
                padding: 0 10px;
            }
        """)

        # file_upload_layout.addWidget(QLabel("File :"))
        file_upload_layout.addWidget(upload_button)
        file_upload_layout.addWidget(self.file_path_display)
        file_upload_layout.addStretch()
        container_layout.addLayout(file_upload_layout)

        self.multiple_device_table = QTableWidget()
        self.multiple_device_table.setColumnCount(1)
        self.multiple_device_table.setHorizontalHeaderLabels(["Code ID and Description"])
        self.multiple_device_table.setColumnWidth(0, 1650)
        self.multiple_device_table.verticalHeader().setVisible(False)
        self.multiple_device_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.multiple_device_table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.multiple_device_table.setStyleSheet("""
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

        container_layout.addWidget(self.multiple_device_table)

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

    def handle_file_upload(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Device List File", "", "Text Files (*.txt)", options=options)

        if file_path:
            self.selected_file_path = file_path
            self.file_path_display.setText(file_path)
            print(f"Selected file: {file_path}")

    def handle_button_click(self, button):
        if not self.selected_file_path:
            self.show_error_message("Please upload a device list file first!")
            return

        try:
            with open(self.selected_file_path, 'r') as f:
                device_list = [line.strip() for line in f.readlines() if line.strip()]

            print("\n--- Selected Devices ---")
            print("\n".join(device_list))
            print("------------------------\n")

        except Exception as e:
            self.show_error_message(f"Error reading file: {str(e)}")
            return

        # Update button styles
        for row in range(self.multiple_device_table.rowCount()):
            widget = self.multiple_device_table.cellWidget(row, 0)
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

        print("\n--- Selection Path ---")
        print(f"Vendor: {self.current_vendor}")
        print(f"Device Type: {self.current_device_type}")
        print(f"Configuration: {self.parent.selected_configuration}")
        print(f"Selected Code: {button.code_id} - {button.description}")
        print("----------------------\n")

        try:
            # Map code IDs to actual script names
            switch_mapping = {
                "0001": "configure_vlan",
                "0002": "show_arp_table",
                "0003": "show_mac_address_table",
                "0004": "show_running_config",
                "0005": "show_vlan_brief"
            }
            
            router_mapping = {
                "1001": "configure_rip",
                "1002": "enable_interface",
                "1003": "enable_ip_routing",
                "1004": "show_ip_route",
                "1005": "show_running_config"
            }
            
            # Choose the correct mapping based on device type
            script_mapping = switch_mapping if self.current_device_type == "switch" else router_mapping
            
            script_filename = script_mapping.get(button.code_id)
            if not script_filename:
                raise ValueError(f"Invalid code ID: {button.code_id}")
                
            script_name = f"Command.Cisco.{self.current_device_type}.{self.current_device_type}_multiple_device.{script_filename}"
            script_module = importlib.import_module(script_name)

            if hasattr(script_module, "main"):
                script_module.main()
            else:
                print(f"Script {script_name} does not define a 'main' function.")
                self.show_error_message(f"Script {script_name} is invalid!")

        except ModuleNotFoundError:
            print(f"Script not found: {script_name}")
            self.show_error_message(f"Script not found: {script_name}")
        except Exception as e:
            print(f"Error running script {script_name}: {e}")
            traceback.print_exc()
            self.show_error_message(f"Error running script: {str(e)}")

        # Clear file input and path after navigating to main page
        self.file_path_display.clear()
        self.selected_file_path = None

        self.parent.open_main_page()

    def set_selected_options(self, vendor, device_type):
        self.current_vendor = vendor
        self.current_device_type = device_type
        self.load_commands()

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

    def load_commands(self):
        if self.current_device_type == "switch":
            self.load_switch_commands()
        elif self.current_device_type == "router":
            self.load_router_commands()

    def load_switch_commands(self):
        commands = [
            ("0001", "configure_vlan"),
            ("0002", "show_arp_table"),
            ("0003", "show_mac_address_table"),
            ("0004", "show_running_config"),
            ("0005", "show_vlan_brief"),
        ]
        self.populate_command_table(commands)

    def load_router_commands(self):
        commands = [
            ("1001", "configure_rip"),
            ("1002", "enable_interface"),
            ("1003", "enable_ip_routing"),
            ("1004", "show_ip_route"),
            ("1005", "show_running_config"),
        ]
        self.populate_command_table(commands)

    def populate_command_table(self, commands):
        self.multiple_device_table.clearContents()
        self.multiple_device_table.setRowCount(len(commands))

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
            button.code_id = code_id
            button.description = description
            button.clicked.connect(lambda checked, b=button: self.handle_button_click(b))

            widget = QWidget()
            layout = QHBoxLayout(widget)
            layout.addWidget(button)
            layout.setContentsMargins(0, 0, 0, 0)

            self.multiple_device_table.setCellWidget(row, 0, widget)
            self.multiple_device_table.setRowHeight(row, 50)

    def show_error_message(self, message):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(message)
        error_dialog.setStandardButtons(QMessageBox.Ok)
        error_dialog.exec_()