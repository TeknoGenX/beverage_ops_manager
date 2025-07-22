import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from core.auth.login import LoginWindow
from core.dashboard.dashboard_controller import DashboardController
from config import init_folders

def main():
    init_folders()

    app = QApplication(sys.argv)
    app.setApplicationName("BeverageOps Manager")

    icon_path = "assets/logo.png"
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    else:
        print("[WARNING] Logo tidak ditemukan:", icon_path)

    # Tampilkan login window
    login_window = LoginWindow()
    if login_window.exec_() == LoginWindow.Accepted:
        user_data = login_window.user_data  # ✅ Ambil dari atribut
        window = DashboardController(user_data)
        window.show()
        sys.exit(app.exec_())
    else:
        print("[INFO] Login dibatalkan.")
        sys.exit()

if __name__ == "__main__":
    main()
