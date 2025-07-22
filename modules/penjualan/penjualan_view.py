# modules/penjualan/penjualan_view.py

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
import os

class PenjualanView(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join("ui", "penjualan.ui"), self)

        # Akses komponen UI
        self.cmbProduk = self.findChild(type(self.cmbProduk), "cmbProduk")
        self.dateEdit = self.findChild(type(self.dateEdit), "dateEdit")
        self.spinQty = self.findChild(type(self.spinQty), "spinQty")
        self.inputArmada = self.findChild(type(self.inputArmada), "inputArmada")
        self.btnTambah = self.findChild(type(self.btnTambah), "btnTambah")
        self.btnHapus = self.findChild(type(self.btnHapus), "btnHapus")
        self.tablePenjualan = self.findChild(type(self.tablePenjualan), "tablePenjualan")

    def make_table_item(self, text):
        item = QTableWidgetItem(text)
        item.setFlags(item.flags() ^ item.flags().ItemIsEditable)
        return item

    def reset_form(self):
        self.cmbProduk.setCurrentIndex(0)
        self.spinQty.setValue(1)
        self.inputArmada.clear()
