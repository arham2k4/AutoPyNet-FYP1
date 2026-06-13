from PyQt5.QtWidgets import (QDialog, QLabel, QLineEdit, QPushButton, 
                             QApplication, QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys
import os

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.main_window = None
        
    def setup_ui(self):
        """Setup the login UI"""
        self.setWindowTitle("AutoPyNet Login")
        self.setGeometry(100, 100, 751, 662)
        
        # Set stylesheet
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                background-color: #007bff;
                color: white;
                font-size: 40px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton {
                font-size: 20px;
                min-height: 40px;
                background-color: green;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: darkgreen;
            }
            QLineEdit {
                font-size: 20px;
                padding: 8px;
                border: 2px solid #007bff;
                border-radius: 5px;
            }
        """)
        
        # Title Label
        title_label = QLabel("Welcome to AutoPyNet")
        title_label.setGeometry(40, 50, 651, 51)
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(32)
        title_font.setBold(True)
        title_label.setFont(title_font)
        
        # Username Label
        username_label = QLabel("Username:")
        username_label.setGeometry(40, 180, 120, 40)
        username_label.setAlignment(Qt.AlignLeft)
        username_label.setStyleSheet("background-color: white; color: black; font-size: 16px;")
        
        # Username Input
        self.username_input = QLineEdit()
        self.username_input.setGeometry(180, 180, 371, 61)
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.textChanged.connect(self.clear_error)
        
        # Password Label
        password_label = QLabel("Password:")
        password_label.setGeometry(40, 270, 120, 40)
        password_label.setAlignment(Qt.AlignLeft)
        password_label.setStyleSheet("background-color: white; color: black; font-size: 16px;")
        
        # Password Input
        self.password_input = QLineEdit()
        self.password_input.setGeometry(180, 270, 371, 61)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.textChanged.connect(self.clear_error)
        
        # Error Label
        self.error_label = QLabel("")
        self.error_label.setGeometry(40, 350, 651, 40)
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setStyleSheet("color: red; font-size: 14px; background-color: white;")
        
        # Login Button
        self.login_button = QPushButton("Login")
        self.login_button.setGeometry(230, 420, 261, 51)
        self.login_button.clicked.connect(self.handle_login)
        
        # Add widgets to dialog
        for widget in [title_label, username_label, self.username_input, 
                      password_label, self.password_input, self.error_label, 
                      self.login_button]:
            widget.setParent(self)
    
    def handle_login(self):
        """Handle login button click"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        # Validate input
        if not username or not password:
            self.show_error("Please enter both username and password")
            return
        
        # Check credentials (admin/admin)
        if username == "admin" and password == "admin":
            self.login_successful()
        elif username == "admin":
            self.show_error("Wrong password. Please enter the correct password.")
            self.password_input.clear()
            self.password_input.setFocus()
        else:
            self.show_error("Invalid username or password")
            self.password_input.clear()
            self.password_input.setFocus()
    
    def show_error(self, message):
        """Display error message"""
        self.error_label.setText(message)
    
    def clear_error(self):
        """Clear error message when user types"""
        self.error_label.setText("")
    
    def login_successful(self):
        """Handle successful login"""
        try:
            # Import main page from the package
            from pages.main_page import AutoPynetDashboard
            print("Login successful: launching dashboard")

            # Create and show main window first, then close the login dialog
            self.main_window = AutoPynetDashboard()
            self.main_window.show()

            # Close login dialog after dashboard is shown
            self.close()

            # Show success message on dashboard
            QMessageBox.information(self.main_window, "Success", "Login successful!")
            
        except ImportError as e:
            import traceback
            traceback.print_exc()
            self.show_error(f"Error loading main page: {str(e)}")
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.show_error(f"An error occurred: {str(e)}")


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Create and show login dialog
    login_dialog = LoginDialog()
    login_dialog.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
