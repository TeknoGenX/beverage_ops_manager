# modules/penjualan/penjualan_model.py

from db.database import Database

class PenjualanModel:
    def __init__(self):
        self.db = Database()

    def tambah_penjualan(self, tanggal, produk_id, qty, harga, total, armada_id):
        query = """
            INSERT INTO penjualan (tanggal, produk_id, qty, harga, total, armada_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        self.db.execute(query, (tanggal, produk_id, qty, harga, total, armada_id))

    def hapus_penjualan(self, penjualan_id):
        query = "DELETE FROM penjualan WHERE id = ?"
        self.db.execute(query, (penjualan_id,))

    def ambil_semua(self):
        query = """
            SELECT p.id, p.tanggal, pr.nama_produk, p.qty, p.harga, p.total, p.armada_id
            FROM penjualan p
            JOIN produk pr ON p.produk_id = pr.id
            ORDER BY p.tanggal DESC
        """
        return self.db.fetchall(query)

    def get_produk_list(self):
        return self.db.fetchall("SELECT id, nama_produk, harga_satuan FROM produk")

    def get_armada_list(self):
        return self.db.fetchall("SELECT DISTINCT armada_id FROM penjualan")
