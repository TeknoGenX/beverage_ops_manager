# modules/distribusi/distribusi_model.py

from db.database import Database

class DistribusiModel:
    def __init__(self):
        self.db = Database()

    def tambah_distribusi(self, tanggal, armada, jumlah_cup, status):
        query = """
            INSERT INTO distribusi (tanggal, armada, jumlah_cup, status)
            VALUES (?, ?, ?, ?)
        """
        self.db.execute(query, (tanggal, armada, jumlah_cup, status))

    def hapus_distribusi(self, distribusi_id):
        query = "DELETE FROM distribusi WHERE id = ?"
        self.db.execute(query, (distribusi_id,))

    def get_semua_distribusi(self):
        query = "SELECT id, tanggal, armada, jumlah_cup, status FROM distribusi ORDER BY tanggal DESC"
        return self.db.fetchall(query)
