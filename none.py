import sys
import time
from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtCore import QTimer

# Import your application classes
from main import AutoPynetDashboard
from pages.vendor_page import VendorPage
from pages.device_type_page import DeviceTypePage
from pages.config_page import ConfigPage
from pages.single_device import SingleDevicePage
from pages.log_window import LogWindow


class AutoPynetAutomator:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = AutoPynetDashboard()
        self.main_window.show()

        self.log_window = LogWindow()

        self.timer = QTimer()
        self.timer.timeout.connect(self.execute_steps)
        self.current_step = 0
        self.timer.start(1000)

    def highlight_button(self, button: QPushButton):
        """Apply hover-like visual effect to a button."""
        if button:
            button.setStyleSheet("""
                QPushButton {
                    border: 2px solid #00bfff;
                    background-color: #e6f7ff;
                    font-weight: bold;
                    color: #000000;
                }
            """)

    def execute_steps(self):
        self.current_step += 1

        if self.current_step == 1:
            print("Step 1: Selecting Cisco as vendor")
            self.log_window.append_log("Step 1: Selecting Cisco as vendor")
            vendor_page = self.main_window.findChild(VendorPage)
            if vendor_page:
                for btn in vendor_page.findChildren(QPushButton):
                    if btn.text() == "Cisco":
                        self.highlight_button(btn)
                        break
                vendor_page.set_vendor_and_navigate("Cisco")

        elif self.current_step == 2:
            print("Step 2: Selecting Switch as device type")
            self.log_window.append_log("Step 2: Selecting Switch as device type")
            device_type_page = self.main_window.findChild(DeviceTypePage)
            if device_type_page:
                for btn in device_type_page.findChildren(QPushButton):
                    if btn.text() == "Switch":
                        self.highlight_button(btn)
                        break
                device_type_page.set_device_type_and_navigate("Switch")

        elif self.current_step == 3:
            print("Step 3: Selecting Single Device configuration")
            self.log_window.append_log("Step 3: Selecting Single Device configuration")
            config_page = self.main_window.findChild(ConfigPage)
            if config_page:
                for btn in config_page.findChildren(QPushButton):
                    if btn.text() == "Single Device":
                        self.highlight_button(btn)
                        break
                config_page.set_configuration_and_navigate("Single Device")

        elif self.current_step == 4:
            print("Step 4: Selecting switch_ping command")
            self.log_window.append_log("Step 4: Selecting switch_ping command")
            single_device_page = self.main_window.findChild(SingleDevicePage)
            if single_device_page:
                single_device_page.set_active_device_type("switch")
                for row in range(single_device_page.single_device_table.rowCount()):
                    widget = single_device_page.single_device_table.cellWidget(row, 0)
                    if widget:
                        button = widget.findChild(QPushButton)
                        if button and "0001 - switch_ping" in button.text():
                            self.highlight_button(button)
                            button.click()
                            self.log_window.append_log("Command 'switch_ping' triggered successfully.")
                            break

        elif self.current_step == 5:
            print("Automation complete.")
            self.log_window.append_log("✅ Automation complete.")
            self.timer.stop()
            self.log_window.show()


if __name__ == '__main__':
    print("Starting AutoPynet automation...")
    automator = AutoPynetAutomator()
    sys.exit(automator.app.exec_())
