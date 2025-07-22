# core/transaksi/transaksi_view.py

from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem
from PyQt5 import uic
from datetime import datetime

from core.transaksi.transaksi_controller import TransaksiController
from db.database import DBKoneksi
from config import log_debug


class TransaksiWindow(QDialog):
    def __init__(self, user_info, parent=None):
        super().__init__(parent)
        uic.loadUi("ui/transaksi.ui", self)
        self.setWindowTitle("Transaksi - BeverageOps Manager")
        self.controller = TransaksiController(self)
        self.user_info = user_info

        self.load_produk()
        self.btnSimpan.clicked.connect(self.simpan_transaksi)
        self.btnBersih.clicked.connect(self.bersihkan_input)

        self.tabelTransaksi.setColumnWidth(1, 200)
        self.load_transaksi_terakhir()

    def load_produk(self):
        """
        Memuat daftar produk ke combo box
        """
        db = DBKoneksi()
        self.comboProduk.clear()
        self.produk_map = {}  # {nama_produk: id}
        data = db.fetchall("SELECT id, nama_produk FROM produk ORDER BY nama_produk ASC")
        for row in data:
            self.comboProduk.addItem(row['nama_produk'])
            self.produk_map[row['nama_produk']] = row['id']
        db.close()

    def simpan_transaksi(self):
        """
        Ambil input user lalu simpan transaksi
        """
        try:
            nama_produk = self.comboProduk.currentText()
            produk_id = self.produk_map.get(nama_produk)
            jumlah = int(self.spinJumlah.value())
            harga_satuan = self.get_harga_produk(produk_id)
            total = harga_satuan * jumlah

            data = {
                "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "produk_id": produk_id,
                "jumlah": jumlah,
                "total_harga": total,
                "kasir": self.user_info.get("username", "unknown")
            }

            berhasil = self.controller.simpan_transaksi(data)
            if berhasil:
                QMessageBox.information(self, "Sukses", "Transaksi berhasil disimpan.")
                self.load_transaksi_terakhir()
                self.bersihkan_input()

        except Exception as e:
            log_debug(f"Gagal menyimpan transaksi: {e}")
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan: {e}")

    def bersihkan_input(self):
        self.spinJumlah.setValue(1)
        self.comboProduk.setCurrentIndex(0)

    def get_harga_produk(self, produk_id):
        db = DBKoneksi()
        row = db.fetchone("SELECT harga FROM produk WHERE id = ?", [produk_id])
        db.close()
        return row["harga"] if row else 0

    def load_transaksi_terakhir(self):
        """
        Tampilkan transaksi terbaru ke tabel
        """
        data = self.controller.ambil_daftar_transaksi(limit=50)
        self.tabelTransaksi.setRowCount(0)
        for row_data in data:
            row_position = self.tabelTransaksi.rowCount()
            self.tabelTransaksi.insertRow(row_position)
            self.tabelTransaksi.setItem(row_position, 0, QTableWidgetItem(str(row_data["id"])))
            self.tabelTransaksi.setItem(row_position, 1, QTableWidgetItem(row_data["tanggal"]))
            self.tabelTransaksi.setItem(row_position, 2, QTableWidgetItem(row_data["nama_produk"]))
            self.tabelTransaksi.setItem(row_position, 3, QTableWidgetItem(str(row_data["jumlah"])))
            self.tabelTransaksi.setItem(row_position, 4, QTableWidgetItem(f"Rp {row_data['total_harga']:,}"))
            self.tabelTransaksi.setItem(row_position, 5, QTableWidgetItem(row_data["kasir"]))
