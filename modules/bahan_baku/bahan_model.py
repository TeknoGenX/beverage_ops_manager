# modules/bahan_baku/bahan_model.py

from db.database import DBKoneksi

class BahanModel:
    def __init__(self):
        self.db = DBKoneksi()

    def semua(self):
        query = """
            SELECT id, nama_bahan, stok_pack, berat_per_pack, sisa_gram, batas_min
            FROM bahan_baku
            ORDER BY nama_bahan
        """
        return self.db.fetchall(query)

    def cari_by_id(self, id_bahan):
        return self.db.fetchone("SELECT * FROM bahan_baku WHERE id = ?", [id_bahan])

    def tambah(self, nama_bahan, stok_pack, berat_per_pack, sisa_gram, batas_min):
        return self.db.insert("bahan_baku", {
            "nama_bahan": nama_bahan,
            "stok_pack": stok_pack,
            "berat_per_pack": berat_per_pack,
            "sisa_gram": sisa_gram,
            "batas_min": batas_min
        })

    def ubah(self, id_bahan, nama_bahan, stok_pack, berat_per_pack, sisa_gram, batas_min):
        query = """
            UPDATE bahan_baku
            SET nama_bahan = ?, stok_pack = ?, berat_per_pack = ?, sisa_gram = ?, batas_min = ?
            WHERE id = ?
        """
        return self.db.execute(query, [nama_bahan, stok_pack, berat_per_pack, sisa_gram, batas_min, id_bahan])

    def hapus(self, id_bahan):
        return self.db.execute("DELETE FROM bahan_baku WHERE id = ?", [id_bahan])

    def __del__(self):
        self.db.close()
