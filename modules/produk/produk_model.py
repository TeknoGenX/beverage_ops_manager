# modules/produk/produk_model.py

from db.database import DBKoneksi

class ProdukModel:
    def __init__(self):
        self.db = DBKoneksi()

    def semua(self):
        """Mengambil semua data produk"""
        query = "SELECT id, nama_produk, harga_satuan FROM produk ORDER BY nama_produk"
        return self.db.fetchall(query)

    def cari_by_id(self, produk_id):
        """Mencari produk berdasarkan ID"""
        return self.db.fetchone("SELECT * FROM produk WHERE id = ?", [produk_id])

    def tambah(self, nama_produk, harga_satuan):
        """Menambahkan produk baru"""
        return self.db.insert("produk", {
            "nama_produk": nama_produk,
            "harga_satuan": harga_satuan
        })

    def ubah(self, produk_id, nama_produk, harga_satuan):
        """Mengupdate data produk"""
        query = "UPDATE produk SET nama_produk = ?, harga_satuan = ? WHERE id = ?"
        return self.db.execute(query, [nama_produk, harga_satuan, produk_id])

    def hapus(self, produk_id):
        """Menghapus produk berdasarkan ID"""
        query = "DELETE FROM produk WHERE id = ?"
        return self.db.execute(query, [produk_id])

    def __del__(self):
        self.db.close()
