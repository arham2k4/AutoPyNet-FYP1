
import sys
from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtCore import QTimer
import os
from PyQt5.QtWidgets import QFileDialog

# Import your application classes
from main import AutoPynetDashboard
from pages.vendor_page import VendorPage
from pages.files_page import FilesPage
from pages.log_window import LogWindow


class SidebarNavigatorAutomator:
    def __init__(self):
        self.app = QApplication(sys.argv)

        # Initialize and show main window (GUI visible)
        self.main_window = AutoPynetDashboard()
        self.main_window.show()

        self.log_window = LogWindow()

        self.timer = QTimer()
        self.timer.timeout.connect(self.execute_steps)
        self.current_step = 0
        self.timer.start(1000)

        # Path to the file to be uploaded
        self.file_path = r"C:\Users\Abdul Moiz Nouman\Desktop\autopynet_dashboard\hello.txt"

        # Store the file dialog object for later use
        self.file_dialog = None

    def highlight_button(self, button: QPushButton):
        """Add a visual effect to the selected button."""
        if button:
            button.setStyleSheet("""
                QPushButton {
                    border: 2px solid #00bfff;
                    background-color: #e6f7ff;
                    font-weight: bold;
                    color: #000000;
                }
            """)

    def click_sidebar_button(self, button_text):
        """Click a button from the sidebar based on its text."""
        for btn in self.main_window.sidebar.findChildren(QPushButton):
            if btn.text() == button_text:
                self.highlight_button(btn)
                btn.click()
                return True
        return False

    def log_step(self, step_number, action_text):
        log_message = (
            f"\n----------------------------\n"
            f"STEP {step_number}\n"
            f"🖱️ Action: Opening {action_text}\n"
            f"Result: Done ✅\n"
            f"----------------------------"
        )
        print(log_message)
        self.log_window.append_log(log_message)

    def upload_file(self):
        """Simulate file upload on 'My Files' page with a delay."""
        self.file_dialog = QFileDialog()
        self.file_dialog.setFileMode(QFileDialog.ExistingFiles)
        self.file_dialog.selectFile(self.file_path)  # Pre-select the file to upload

        if self.file_dialog.exec_():
            selected_files = self.file_dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                self.log_step(4, f"Preparing to upload file: {file_path}")

                # Add a 7-second delay before proceeding with the upload
                QTimer.singleShot(7000, lambda: self.simulate_file_upload(file_path))
                return True
        return False

    def simulate_file_upload(self, file_path):
        """Simulate file upload process after the delay."""
        self.log_step(4, f"File selected: {file_path}")
        self.log_step(4, f"Uploading file: {file_path}...")

        # Simulate the upload process
        # Here, you can call the actual upload function or perform necessary operations
        self.upload_file_done(file_path)

    def upload_file_done(self, file_path):
        """Complete the file upload process."""
        self.log_step(4, f"File uploaded successfully: {file_path}")

        # Simulate clicking on the uploaded file and viewing content
        self.log_step(4, "Clicking on the uploaded file to view its content.")
        self.log_step(4, "File content previewed.")

        # Simulate deleting the uploaded file
        self.delete_file()

    def delete_file(self):
        """Simulate file deletion from 'My Files' page."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)  # Delete the file from disk
            self.log_step(5, f"File deleted: {self.file_path}")
            return True
        return False

    def execute_steps(self):
        """Go through each sidebar navigation step."""
        self.current_step += 1

        if self.current_step == 1:
            self.log_step(1, "Dashboard (Home)")
            self.click_sidebar_button("Dashboard")

        elif self.current_step == 2:
            self.log_step(2, "Vendor")
            self.click_sidebar_button("Vendor")

        elif self.current_step == 3:
            self.log_step(3, "Dashboard (Home)")
            self.click_sidebar_button("Dashboard")

        elif self.current_step == 4:
            self.log_step(4, "My Files")
            self.click_sidebar_button("My Files")

            # Simulate uploading a file
            if self.upload_file():
                self.log_step(4, "Waiting 7 seconds before uploading the file...")

        elif self.current_step == 5:
            self.log_step(5, "Dashboard (Home)")
            self.click_sidebar_button("Dashboard")

        elif self.current_step == 6:
            self.log_step(6, "Logs")
            self.click_sidebar_button("Logs")

        elif self.current_step == 7:
            final_msg = "\nAll steps completed successfully. ✅\n"
            print(final_msg)
            self.log_window.append_log(final_msg)
            self.timer.stop()
            self.log_window.show()


if __name__ == '__main__':
    print("Launching sidebar navigator...\n")
    automator = SidebarNavigatorAutomator()
    sys.exit(automator.app.exec_())
