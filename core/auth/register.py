# core/auth/register.py

import os
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import uic

from db.database import DBKoneksi
from core.utils.hash import hash_password
from config import ROLE, log_debug

class RegisterWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        ui_path = "ui/register.ui"
        if not os.path.exists(ui_path):
            QMessageBox.critical(self, "Error", f"File UI tidak ditemukan: {ui_path}")
            raise FileNotFoundError(f"UI file '{ui_path}' tidak ditemukan.")

        uic.loadUi(ui_path, self)
        self.setWindowTitle("Registrasi Pengguna")

        self.comboRole.addItems(ROLE.keys())
        self.btnRegister.clicked.connect(self.daftar_user)

    def daftar_user(self):
        username = self.txtUsername.text().strip()
        password = self.txtPassword.text().strip()
        role = self.comboRole.currentText()

        # Validasi input
        if not username or not password:
            QMessageBox.warning(self, "Validasi Gagal", "Semua kolom wajib diisi.")
            return

        if len(password) < 6:
            QMessageBox.warning(self, "Password Lemah", "Password minimal 6 karakter.")
            return

        # Hash password
        password_hash = hash_password(password)

        # Simpan ke database
        db = DBKoneksi()
        try:
            existing = db.fetchone("SELECT * FROM users WHERE username = ?", [username])
            if existing:
                QMessageBox.critical(self, "Gagal", "Username sudah digunakan.")
                return

            berhasil = db.insert("users", {
                "username": username,
                "password_hash": password_hash,
                "role": role
            })

            if berhasil:
                log_debug(f"Registrasi berhasil untuk user: {username}")
                QMessageBox.information(self, "Berhasil", f"User '{username}' berhasil ditambahkan.")
                self.accept()
            else:
                QMessageBox.critical(self, "Gagal", "Gagal menyimpan data ke database.")
        except Exception as e:
            log_debug(f"Error saat registrasi: {e}")
            QMessageBox.critical(self, "Error", "Terjadi kesalahan saat registrasi.")
        finally:
            db.close()
