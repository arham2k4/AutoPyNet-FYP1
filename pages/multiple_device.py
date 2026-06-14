import importlib
import traceback
from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QTableWidget, QTableWidgetItem, QWidget, QMessageBox,
                             QFileDialog, QLineEdit)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
import threading


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

        # Disable the command table to avoid repeated clicks and UI churn
        self._set_buttons_enabled(False)

        # If a real QPushButton was passed, provide a visual highlight; otherwise skip
        if hasattr(button, 'setEnabled'):
            try:
                button.setEnabled(False)
            except Exception:
                pass
        if hasattr(button, 'setStyleSheet'):
            try:
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
                """)
            except Exception:
                pass

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
                "0005": "show_vlan_brief",
            }
            
            router_mapping = {
                "1001": "configure_rip",
                "1002": "enable_interface",
                "1003": "enable_ip_routing",
                "1004": "show_ip_route",
                "1005": "show_running_config",
            }

            script_mapping = switch_mapping if self.current_device_type == "switch" else router_mapping
            script_filename = script_mapping.get(button.code_id)
            if not script_filename:
                raise ValueError(f"Invalid code ID: {button.code_id}")

            script_name = f"Command.Cisco.{self.current_device_type}.{self.current_device_type}_multiple_device.{script_filename}"

            # Run import and execution in background to avoid blocking the UI
            thread = threading.Thread(
                target=self._run_multiple_script,
                args=(script_name, device_list, button.code_id, button.description),
                daemon=True,
            )
            thread.start()

        except ModuleNotFoundError as e:
            msg = f"Module not found: {e}"
            print(msg)
            self.parent.log_message(msg)
            self.show_error_message(f"Required module missing: {e}")
            self._set_buttons_enabled(True)
        except Exception as e:
            msg = f"Error preparing script {button.code_id}: {e}"
            print(msg)
            traceback.print_exc()
            self.parent.log_message(msg)
            self.show_error_message(f"Error: {str(e)}")
            self._set_buttons_enabled(True)

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
        # Use lightweight QTableWidgetItem entries instead of embedding QPushButton widgets
        # to avoid heavy widget creation when the command list is large.
        self.multiple_device_table.clearContents()
        self.multiple_device_table.setRowCount(len(commands))

        for row, (code_id, description) in enumerate(commands):
            item_text = f"{code_id} - {description}"
            item = QTableWidgetItem(item_text)
            item.setData(Qt.UserRole, (code_id, description))
            item.setFont(QFont("Arial", 12))
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            self.multiple_device_table.setItem(row, 0, item)
            self.multiple_device_table.setRowHeight(row, 50)

        # Connect click handler to process commands when a row is clicked
        try:
            # avoid reconnecting multiple times
            self.multiple_device_table.cellClicked.disconnect()
        except Exception:
            pass
        self.multiple_device_table.cellClicked.connect(self.handle_table_click)

    def _run_multiple_script(self, script_name, device_list, code_id, description):
        try:
            script_module = importlib.import_module(script_name)

            if hasattr(script_module, "main"):
                try:
                    # Call main() in module; module is responsible for handling multiple devices
                    script_module.main()
                    self.parent.log_message(f"Command executed: {code_id} - {description}")
                except Exception as exec_err:
                    err = f"Execution error in {script_name}: {exec_err}"
                    print(err)
                    self.parent.log_message(err)
            else:
                msg = f"Script {script_name} does not define a 'main' function."
                print(msg)
                self.parent.log_message(msg)
                # Show error on UI thread
                QTimer.singleShot(0, lambda: self.show_error_message(f"Script {script_name} is invalid!"))
        except ModuleNotFoundError as e:
            msg = f"Module not found: {e}"
            print(msg)
            self.parent.log_message(msg)
            QTimer.singleShot(0, lambda: self.show_error_message(f"Required module missing: {e}"))
        except Exception as e:
            msg = f"Error running script {script_name}: {e}"
            print(msg)
            traceback.print_exc()
            self.parent.log_message(msg)
            QTimer.singleShot(0, lambda: self.show_error_message(f"Error running script: {str(e)}"))
        finally:
            # Clear file input and path on UI thread and re-enable buttons
            QTimer.singleShot(0, lambda: self.file_path_display.clear())
            QTimer.singleShot(0, lambda: setattr(self, 'selected_file_path', None))
            QTimer.singleShot(0, self._set_buttons_enabled)

    def _set_buttons_enabled(self, enabled=True):
        # Enable/disable the whole command table to prevent interaction during background runs
        try:
            self.multiple_device_table.setEnabled(enabled)
        except Exception:
            pass

    def show_error_message(self, message):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(message)
        error_dialog.setStandardButtons(QMessageBox.Ok)
        error_dialog.exec_()

    def handle_table_click(self, row, column):
        """Triggered when a table row is clicked; extract code and description and run."""
        item = self.multiple_device_table.item(row, 0)
        if not item:
            return
        data = item.data(Qt.UserRole)
        if not data:
            return
        code_id, description = data

        # Create a minimal button-like object to reuse existing flow where helpful
        class _BtnObj:
            pass

        btn = _BtnObj()
        btn.code_id = code_id
        btn.description = description

        # Delegate to handle_button_click which will start the background thread
        # and manage UI disabling. We adapt by calling the same logic path.
        self.handle_button_click(btn)