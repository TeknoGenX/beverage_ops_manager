# core/auth/user_manage.py

import os
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem
from PyQt5 import uic

from db.database import DBKoneksi
from core.utils.hash import hash_password
from config import ROLE, log_debug

class UserManageWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        ui_path = "ui/user_manage.ui"
        if not os.path.exists(ui_path):
            QMessageBox.critical(self, "Error", f"File UI tidak ditemukan: {ui_path}")
            raise FileNotFoundError(f"UI file '{ui_path}' tidak ditemukan.")

        uic.loadUi(ui_path, self)
        self.setWindowTitle("Manajemen Pengguna")

        self.btnTambah.clicked.connect(self.tambah_user)
        self.btnHapus.clicked.connect(self.hapus_user)
        self.tableUsers.itemSelectionChanged.connect(self.tampilkan_user_terpilih)

        self.load_data()

    def load_data(self):
        self.tableUsers.setRowCount(0)
        db = DBKoneksi()
        users = db.fetchall("SELECT id, username, role FROM users ORDER BY username ASC")
        db.close()

        for row_idx, user in enumerate(users):
            self.tableUsers.insertRow(row_idx)
            self.tableUsers.setItem(row_idx, 0, QTableWidgetItem(str(user['id'])))
            self.tableUsers.setItem(row_idx, 1, QTableWidgetItem(user['username']))
            self.tableUsers.setItem(row_idx, 2, QTableWidgetItem(user['role']))

        log_debug("Berhasil memuat data user")

    def tampilkan_user_terpilih(self):
        selected = self.tableUsers.selectedItems()
        if selected:
            self.txtUsername.setText(selected[1].text())
            idx = self.comboRole.findText(selected[2].text())
            self.comboRole.setCurrentIndex(idx)

    def tambah_user(self):
        username = self.txtUsername.text().strip()
        password = self.txtPassword.text().strip()
        role = self.comboRole.currentText()

        if not username or not password:
            QMessageBox.warning(self, "Validasi Gagal", "Isi semua kolom.")
            return

        if len(password) < 6:
            QMessageBox.warning(self, "Password Lemah", "Minimal 6 karakter.")
            return

        db = DBKoneksi()
        existing = db.fetchone("SELECT * FROM users WHERE username = ?", [username])
        if existing:
            QMessageBox.critical(self, "Gagal", "Username sudah digunakan.")
            db.close()
            return

        password_hash = hash_password(password)
        berhasil = db.insert("users", {
            "username": username,
            "password_hash": password_hash,
            "role": role
        })
        db.close()

        if berhasil:
            log_debug(f"User baru ditambahkan: {username}")
            QMessageBox.information(self, "Berhasil", "User berhasil ditambahkan.")
            self.load_data()
            self.txtUsername.clear()
            self.txtPassword.clear()
        else:
            QMessageBox.critical(self, "Gagal", "Gagal menambahkan user.")

    def hapus_user(self):
        selected = self.tableUsers.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Pilih User", "Pilih user yang ingin dihapus.")
            return

        user_id = selected[0].text()
        username = selected[1].text()

        konfirmasi = QMessageBox.question(
            self, "Konfirmasi",
            f"Yakin ingin menghapus user '{username}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if konfirmasi == QMessageBox.Yes:
            db = DBKoneksi()
            berhasil = db.delete("users", "id = ?", [user_id])
            db.close()

            if berhasil:
                log_debug(f"User dihapus: {username}")
                QMessageBox.information(self, "Berhasil", "User berhasil dihapus.")
                self.load_data()
                self.txtUsername.clear()
                self.txtPassword.clear()
            else:
                QMessageBox.critical(self, "Gagal", "Gagal menghapus user.")
