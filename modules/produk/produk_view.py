# modules/produk/produk_view.py

from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from PyQt5 import uic
from modules.produk.produk_controller import ProdukController

class ProdukView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("ui/produk.ui", self)
        self.controller = ProdukController(self)

    def make_item(self, text):
        """Helper untuk buat item tabel yang tidak bisa diedit"""
        item = QTableWidgetItem(text)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        return item
