# modules/penjualan/penjualan_controller.py

from PyQt5.QtWidgets import QMessageBox
from modules.penjualan.penjualan_model import PenjualanModel

class PenjualanController:
    def __init__(self, view):
        self.view = view
        self.model = PenjualanModel()
        self.load_produk()
        self.load_data_penjualan()
        self.setup_events()

    def setup_events(self):
        self.view.btnTambah.clicked.connect(self.tambah_penjualan)
        self.view.btnHapus.clicked.connect(self.hapus_penjualan)

    def load_produk(self):
        self.view.cmbProduk.clear()
        produk_list = self.model.get_produk_list()
        for id_produk, nama_produk, harga in produk_list:
            self.view.cmbProduk.addItem(f"{nama_produk} - Rp{harga:,}", id_produk)

    def load_data_penjualan(self):
        self.view.tablePenjualan.setRowCount(0)
        data = self.model.ambil_semua()
        for row_idx, row in enumerate(data):
            self.view.tablePenjualan.insertRow(row_idx)
            for col_idx, item in enumerate(row):
                self.view.tablePenjualan.setItem(row_idx, col_idx, self.view.make_table_item(str(item)))

    def tambah_penjualan(self):
        tanggal = self.view.dateEdit.date().toString("yyyy-MM-dd")
        produk_idx = self.view.cmbProduk.currentIndex()
        produk_id = self.view.cmbProduk.itemData(produk_idx)
        qty = self.view.spinQty.value()

        if produk_id is None or qty <= 0:
            QMessageBox.warning(self.view, "Validasi", "Pilih produk dan jumlah yang valid.")
            return

        produk_data = self.model.get_produk_list()[produk_idx]
        harga = produk_data[2]
        total = harga * qty
        armada_id = self.view.inputArmada.text()

        self.model.tambah_penjualan(tanggal, produk_id, qty, harga, total, armada_id)
        self.load_data_penjualan()
        self.view.reset_form()

    def hapus_penjualan(self):
        selected = self.view.tablePenjualan.currentRow()
        if selected == -1:
            QMessageBox.warning(self.view, "Hapus Data", "Pilih baris yang ingin dihapus.")
            return
        id_penjualan = self.view.tablePenjualan.item(selected, 0).text()
        self.model.hapus_penjualan(id_penjualan)
        self.load_data_penjualan()
