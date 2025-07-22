import os
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic
import bcrypt

from config import log_debug

try:
    from db.database import DBKoneksi
except ImportError:
    DBKoneksi = None
    log_debug("Gagal mengimpor DBKoneksi dari db/database.py")


class LoginWindow(QDialog):
    login_berhasil = pyqtSignal(dict)  # sinyal ke main.py jika login sukses

    def __init__(self, parent=None):
        super().__init__(parent)
        ui_path = "ui/login.ui"

        if not os.path.exists(ui_path):
            QMessageBox.critical(self, "Error", f"UI file tidak ditemukan: {ui_path}")
            raise FileNotFoundError(f"File UI {ui_path} tidak ditemukan.")

        uic.loadUi(ui_path, self)
        self.setWindowTitle("Login - BeverageOps Manager")

        self.btnLogin.clicked.connect(self.cek_login)
        self.txtPassword.returnPressed.connect(self.cek_login)

    def cek_login(self):
        username = self.txtUsername.text().strip()
        password = self.txtPassword.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Login Gagal", "Harap isi username dan password.")
            return

        if DBKoneksi is None:
            QMessageBox.critical(self, "Error", "Koneksi ke database gagal.")
            return

        try:
            db = DBKoneksi()
        except Exception as e:
            log_debug(f"Gagal membuat koneksi DB: {e}")
            QMessageBox.critical(self, "Database Error", "Tidak dapat menghubungi database.")
            return

        try:
            user = db.fetchone("SELECT * FROM users WHERE username = ?", [username])
        except Exception as e:
            log_debug(f"DB error saat login: {e}")
            QMessageBox.critical(self, "Database Error", "Gagal mengakses database.")
            return
        finally:
            db.close()

        if not user:
            QMessageBox.critical(self, "Login Gagal", "Username tidak ditemukan.")
            return

        # Verifikasi password hash
        try:
            if 'password_hash' not in user:
                log_debug("Kolom password_hash tidak ditemukan dalam data pengguna.")
                QMessageBox.critical(self, "Error", "Struktur data pengguna tidak valid.")
                return

            password_hash = user['password_hash']
            if bcrypt.checkpw(password.encode(), password_hash.encode()):
                log_debug(f"Login berhasil oleh: {username}")

                # ✅ Tambahkan data pengguna agar bisa diakses di main.py
                self.user_data = {
                    "username": user["username"],
                    "role": user["role"]
                }

                self.login_berhasil.emit(user)  # sinyal opsional
                self.accept()  # tutup dialog
            else:
                QMessageBox.critical(self, "Login Gagal", "Password salah.")
        except Exception as e:
            log_debug(f"Error verifikasi password: {e}")
            QMessageBox.critical(self, "Error", "Terjadi kesalahan saat login.")
