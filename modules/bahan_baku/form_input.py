# File: modules/bahan_baku/form_input.py
from PyQt5.QtCore import pyqtSignal

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox
)

class BahanBakuForm(QWidget):
    # Signal emitted when form is submitted successfully
    form_submitted = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.form_layout = QFormLayout()

        self.nama_input = QLineEdit()
        self.stok_input = QLineEdit()
        self.satuan_input = QLineEdit()
        self.harga_input = QLineEdit()

        self.form_layout.addRow(QLabel("Nama Bahan Baku:"), self.nama_input)
        self.form_layout.addRow(QLabel("Stok:"), self.stok_input)
        self.form_layout.addRow(QLabel("Satuan:"), self.satuan_input)
        self.form_layout.addRow(QLabel("Harga per Satuan:"), self.harga_input)

        self.submit_btn = QPushButton("Simpan")
        self.submit_btn.clicked.connect(self.submit_form)

        self.layout.addLayout(self.form_layout)
        self.layout.addWidget(self.submit_btn)
        self.setLayout(self.layout)

    def submit_form(self):
        nama = self.nama_input.text().strip()
        stok = self.stok_input.text().strip()
        satuan = self.satuan_input.text().strip()
        harga = self.harga_input.text().strip()

        if not nama or not stok or not satuan or not harga:
            QMessageBox.warning(self, "Input Error", "Semua field harus diisi.")
            return

        try:
            stok_val = float(stok)
            harga_val = float(harga)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Stok dan Harga harus berupa angka.")
            return

        data = {
            "nama": nama,
            "stok": stok_val,
            "satuan": satuan,
            "harga": harga_val
        }

        self.form_submitted.emit(data)
        QMessageBox.information(self, "Sukses", "Data bahan baku berhasil disimpan.")
        self.clear_form()

    def clear_form(self):
        self.nama_input.clear()
        self.stok_input.clear()
        self.satuan_input.clear()
        self.harga_input.clear()