# modules/distribusi/distribusi_view.py

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import Qt
from modules.distribusi.distribusi_controller import DistribusiController

class DistribusiView(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/distribusi.ui", self)
        self.controller = DistribusiController(self)

        self.btnTambah.clicked.connect(self.aksi_tambah)
        self.btnHapus.clicked.connect(self.aksi_hapus)

        self.tableDistribusi.setColumnWidth(1, 120)
        self.tableDistribusi.setColumnWidth(2, 150)
        self.tableDistribusi.setColumnWidth(3, 100)
        self.tableDistribusi.setColumnWidth(4, 100)

    def tampilkan_data_distribusi(self, data):
        self.tableDistribusi.setRowCount(0)
        for row_data in data:
            row_index = self.tableDistribusi.rowCount()
            self.tableDistribusi.insertRow(row_index)
            for col_index, item in enumerate(row_data):
                self.tableDistribusi.setItem(row_index, col_index, self._buat_item(item))

    def _buat_item(self, teks):
        from PyQt5.QtWidgets import QTableWidgetItem
        item = QTableWidgetItem(str(teks))
        item.setTextAlignment(Qt.AlignCenter)
        return item

    def aksi_tambah(self):
        tanggal = self.inputTanggal.text()
        armada = self.inputArmada.text()
        jumlah = self.inputJumlah.text()
        status = self.comboStatus.currentText()

        self.controller.tambah_distribusi(tanggal, armada, jumlah, status)

    def aksi_hapus(self):
        selected = self.tableDistribusi.currentRow()
        if selected >= 0:
            distribusi_id = self.tableDistribusi.item(selected, 0).text()
            self.controller.hapus_distribusi(distribusi_id)
        else:
            self.tampilkan_pesan("Pilih baris yang ingin dihapus.")

    def tampilkan_pesan(self, pesan):
        QMessageBox.information(self, "Informasi", pesan)
