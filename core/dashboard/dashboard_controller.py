# core/dashboard/dashboard_controller.py

import os
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic

from config import log_debug, ROLE
from core.dashboard.dashboard_view import DashboardView

class DashboardController(QMainWindow):
    def __init__(self, user, parent=None):
        super().__init__(parent)

        self.user = user
        ui_path = "ui/dashboard.ui"
        if not os.path.exists(ui_path):
            QMessageBox.critical(self, "Error", f"UI dashboard tidak ditemukan: {ui_path}")
            raise FileNotFoundError(f"File {ui_path} tidak ditemukan.")

        uic.loadUi(ui_path, self)
        self.setWindowTitle("Dashboard - BeverageOps Manager")

        self.labelWelcome.setText(f"Selamat datang, {user['username']}!")
        role_str = ROLE.get(user['role'], user['role'])
        self.labelRole.setText(f"Peran: {role_str}")

        self.dashboard_view = DashboardView(self)
        self.init_dashboard()

    def init_dashboard(self):
        log_debug(f"Memuat dashboard untuk {self.user['username']} dengan role {self.user['role']}")

        # Tampilkan fitur berdasarkan role
        role = self.user['role']

        if role == "admin":
            self.dashboard_view.tampilkan_admin_panel()
        elif role == "supervisor":
            self.dashboard_view.tampilkan_supervisor_panel()
        elif role == "kasir":
            self.dashboard_view.tampilkan_kasir_panel()
        elif role == "staff":
            self.dashboard_view.tampilkan_gudang_panel()
        else:
            QMessageBox.warning(self, "Peran Tidak Dikenal", f"Role '{role}' tidak dikenali.")
