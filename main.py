# main.py
from PyQt5.QtWidgets import QApplication
import sys
from pages.login import LoginDialog

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Show login dialog first; dashboard opens after successful login
    login_dialog = LoginDialog()
    login_dialog.show()

    try:
        sys.exit(app.exec_())
    except Exception as e:
        print(f"CRASHED: {e}", file=sys.stderr)
        raise

