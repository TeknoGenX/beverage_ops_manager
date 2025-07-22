# db/database.py

import sqlite3
from config import PATH_DATABASE, log_debug

class DBKoneksi:
    def __init__(self, path=PATH_DATABASE):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def fetchall(self, query, params=None):
        """Ambil semua baris hasil query"""
        try:
            self.cursor.execute(query, params or [])
            hasil = self.cursor.fetchall()
            return [dict(row) for row in hasil]
        except Exception as e:
            log_debug(f"fetchall error: {e}")
            return []

    def fetchone(self, query, params=None):
        """Ambil satu baris hasil query"""
        try:
            self.cursor.execute(query, params or [])
            hasil = self.cursor.fetchone()
            return dict(hasil) if hasil else None
        except Exception as e:
            log_debug(f"fetchone error: {e}")
            return None

    def execute(self, query, params=None):
        """Eksekusi query (insert/update/delete)"""
        try:
            self.cursor.execute(query, params or [])
            self.conn.commit()
            return True
        except Exception as e:
            log_debug(f"execute error: {e}")
            return False

    def insert(self, table, data: dict):
        """Insert data ke tabel tertentu"""
        keys = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        query = f"INSERT INTO {table} ({keys}) VALUES ({placeholders})"
        return self.execute(query, list(data.values()))

    def update(self, table, data: dict, where: str, where_params: list):
        """Update data berdasarkan kondisi"""
        set_clause = ', '.join([f"{key}=?" for key in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where}"
        return self.execute(query, list(data.values()) + where_params)

    def delete(self, table, where: str, where_params: list):
        """Hapus data dari tabel berdasarkan kondisi"""
        query = f"DELETE FROM {table} WHERE {where}"
        return self.execute(query, where_params)

    def close(self):
        self.conn.close()
