# modules/produk/produk_controller.py

from PyQt5.QtWidgets import QMessageBox
from modules.produk.produk_model import ProdukModel

class ProdukController:
    def __init__(self, ui):
        self.ui = ui
        self.model = ProdukModel()
        self.produk_aktif_id = None
        self.setup_ui()

    def setup_ui(self):
        self.ui.btnSimpan.clicked.connect(self.simpan_produk)
        self.ui.btnReset.clicked.connect(self.reset_form)
        self.ui.btnHapus.clicked.connect(self.hapus_produk)
        self.ui.tblProduk.itemSelectionChanged.connect(self.tampil_detail)

        self.load_data()

    def load_data(self):
        self.ui.tblProduk.setRowCount(0)
        for row_idx, (id_produk, nama, harga) in enumerate(self.model.semua()):
            self.ui.tblProduk.insertRow(row_idx)
            self.ui.tblProduk.setItem(row_idx, 0, self.ui.make_item(str(id_produk)))
            self.ui.tblProduk.setItem(row_idx, 1, self.ui.make_item(nama))
            self.ui.tblProduk.setItem(row_idx, 2, self.ui.make_item(f"Rp {harga:,.0f}"))

    def simpan_produk(self):
        nama = self.ui.txtNama.text().strip()
        harga = self.ui.spinHarga.value()

        if not nama:
            QMessageBox.warning(self.ui, "Validasi", "Nama produk tidak boleh kosong.")
            return

        if self.produk_aktif_id:
            self.model.ubah(self.produk_aktif_id, nama, harga)
            QMessageBox.information(self.ui, "Berhasil", "Data produk berhasil diubah.")
        else:
            self.model.tambah(nama, harga)
            QMessageBox.information(self.ui, "Berhasil", "Produk baru berhasil ditambahkan.")

        self.reset_form()
        self.load_data()

    def tampil_detail(self):
        selected = self.ui.tblProduk.selectedItems()
        if not selected:
            return

        self.produk_aktif_id = int(selected[0].text())
        nama = selected[1].text()
        harga_text = selected[2].text().replace("Rp", "").replace(",", "").strip()

        self.ui.txtNama.setText(nama)
        self.ui.spinHarga.setValue(int(harga_text))

    def hapus_produk(self):
        if not self.produk_aktif_id:
            QMessageBox.warning(self.ui, "Peringatan", "Pilih produk yang ingin dihapus.")
            return

        confirm = QMessageBox.question(
            self.ui, "Konfirmasi", "Yakin ingin menghapus produk ini?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            self.model.hapus(self.produk_aktif_id)
            self.reset_form()
            self.load_data()

    def reset_form(self):
        self.ui.txtNama.clear()
        self.ui.spinHarga.setValue(0)
        self.ui.tblProduk.clearSelection()
        self.produk_aktif_id = None
