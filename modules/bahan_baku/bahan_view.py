# modules/bahan_baku/bahan_view.py

from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
import os

from modules.bahan_baku.bahan_controller import BahanController

class BahanView(QWidget):
    def __init__(self):
        super().__init__()
        loadUi(os.path.join('ui', 'bahan_baku.ui'), self)

        self.controller = BahanController(self)
        self.editing_id = None

        self.btnSimpan.clicked.connect(self.controller.simpan)
        self.btnHapus.clicked.connect(self.controller.hapus)
        self.btnEdit.clicked.connect(self.controller.muat_untuk_edit)
        self.tabel.cellClicked.connect(self.on_row_clicked)

    def validasi_input(self):
        if not self.inputNama.text().strip():
            QMessageBox.warning(self, "Validasi", "Nama bahan tidak boleh kosong.")
            return False
        if not self.inputPack.text().isdigit() or not self.inputBerat.text().isdigit():
            QMessageBox.warning(self, "Validasi", "Pack dan berat harus berupa angka.")
            return False
        return True

    def get_input_data(self):
        return (
            self.inputNama.text(),
            int(self.inputPack.text()),
            int(self.inputBerat.text()),
            int(self.inputSisaGram.text()),
            int(self.inputBatas.text())
        )

    def set_input_data(self, data):
        self.inputNama.setText(data[1])
        self.inputPack.setText(str(data[2]))
        self.inputBerat.setText(str(data[3]))
        self.inputSisaGram.setText(str(data[4]))
        self.inputBatas.setText(str(data[5]))

    def clear_input(self):
        self.inputNama.clear()
        self.inputPack.clear()
        self.inputBerat.clear()
        self.inputSisaGram.clear()
        self.inputBatas.clear()
        self.editing_id = None

    def tambah_ke_tabel(self, row_data):
        row = self.tabel.rowCount()
        self.tabel.insertRow(row)
        for i, val in enumerate(row_data):
            self.tabel.setItem(row, i, self._make_item(str(val)))

    def _make_item(self, text):
        from PyQt5.QtWidgets import QTableWidgetItem
        item = QTableWidgetItem(text)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        return item

    def get_selected_id(self):
        row = self.tabel.currentRow()
        if row >= 0:
            return int(self.tabel.item(row, 0).text())
        return None

    def on_row_clicked(self, row, column):
        self.tabel.selectRow(row)
