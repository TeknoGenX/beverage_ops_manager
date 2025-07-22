# modules/laporan/laporan_model.py

from db.database import Database

class LaporanModel:
    def __init__(self):
        self.db = Database()

    def get_laporan_penjualan(self, tanggal_awal, tanggal_akhir):
        query = """
        SELECT p.tanggal, pr.nama_produk, p.qty, p.harga, p.total, p.armada_id
        FROM penjualan p
        JOIN produk pr ON p.produk_id = pr.id
        WHERE p.tanggal BETWEEN ? AND ?
        ORDER BY p.tanggal
        """
        return self.db.fetch_all(query, (tanggal_awal, tanggal_akhir))

    def get_laporan_distribusi(self, tanggal_awal, tanggal_akhir):
        query = """
        SELECT * FROM distribusi
        WHERE tanggal BETWEEN ? AND ?
        """
        return self.db.fetch_all(query, (tanggal_awal, tanggal_akhir))
