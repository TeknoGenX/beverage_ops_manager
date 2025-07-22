# core/transaksi/transaksi_controller.py

from PyQt5.QtWidgets import QMessageBox
from datetime import datetime

from db.database import DBKoneksi
from config import log_debug


class TransaksiController:
    def __init__(self, parent=None):
        self.parent = parent  # jendela yang memanggil (optional)

    def simpan_transaksi(self, data: dict) -> bool:
        """
        Simpan transaksi ke database.
        data harus berisi: tanggal, produk_id, jumlah, total_harga, kasir
        """
        try:
            # Validasi sederhana
            if not all(k in data for k in ("tanggal", "produk_id", "jumlah", "total_harga", "kasir")):
                raise ValueError("Data transaksi tidak lengkap.")

            if data["jumlah"] <= 0 or data["total_harga"] <= 0:
                raise ValueError("Jumlah dan total harga harus lebih dari 0.")

            db = DBKoneksi()
            berhasil = db.insert("transaksi", {
                "tanggal": data["tanggal"],
                "produk_id": data["produk_id"],
                "jumlah": data["jumlah"],
                "total_harga": data["total_harga"],
                "kasir": data["kasir"]
            })
            db.close()

            if not berhasil:
                raise Exception("Gagal menyimpan transaksi ke database.")

            log_debug(f"Transaksi berhasil disimpan: {data}")
            return True

        except Exception as e:
            log_debug(f"Error simpan transaksi: {e}")
            if self.parent:
                QMessageBox.critical(self.parent, "Error", str(e))
            return False

    def ambil_daftar_transaksi(self, limit=100):
        """
        Mengambil daftar transaksi terbaru.
        """
        db = DBKoneksi()
        hasil = db.fetchall(
            "SELECT t.id, t.tanggal, p.nama_produk, t.jumlah, t.total_harga, t.kasir "
            "FROM transaksi t JOIN produk p ON t.produk_id = p.id "
            "ORDER BY t.tanggal DESC LIMIT ?", [limit]
        )
        db.close()
        return hasil or []
