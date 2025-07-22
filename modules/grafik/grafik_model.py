# modules/grafik/grafik_model.py

from db.database import Database

class GrafikModel:
    def __init__(self):
        self.db = Database()

    def penjualan_per_produk(self, tanggal_mulai=None, tanggal_akhir=None):
        query = """
            SELECT produk.nama_produk, SUM(penjualan.qty) AS total_terjual
            FROM penjualan
            JOIN produk ON penjualan.produk_id = produk.id
        """
        params = []

        if tanggal_mulai and tanggal_akhir:
            query += " WHERE tanggal BETWEEN ? AND ?"
            params.extend([tanggal_mulai, tanggal_akhir])

        query += " GROUP BY produk.nama_produk ORDER BY total_terjual DESC"

        return self.db.fetchall(query, params)

    def pemakaian_bahan_per_bulan(self):
        query = """
            SELECT strftime('%Y-%m', tanggal) AS bulan, bahan_baku.nama_bahan, SUM(pemakaian.jumlah_gram) AS total_pemakaian
            FROM pemakaian
            JOIN bahan_baku ON pemakaian.bahan_id = bahan_baku.id
            GROUP BY bulan, bahan_baku.nama_bahan
            ORDER BY bulan DESC
        """
        return self.db.fetchall(query)

    def armada_terbaik(self):
        query = """
            SELECT armada, SUM(total) AS total_penjualan
            FROM penjualan
            GROUP BY armada
            ORDER BY total_penjualan DESC
            LIMIT 1
        """
        return self.db.fetchone(query)
