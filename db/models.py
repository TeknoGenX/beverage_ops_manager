# db/models.py

import sqlite3
from config import PATH_DATABASE, log_debug

class Database:
    def __init__(self, path=PATH_DATABASE):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row  # hasil berupa dict
        self.cursor = self.conn.cursor()
        self.inisialisasi_tabel()

    def inisialisasi_tabel(self):
        """Buat tabel-tabel utama jika belum ada"""
        log_debug("Membuat tabel jika belum tersedia...")

        # Tabel User
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
        )
        """)

        # Tabel Produk
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS produk (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_produk TEXT NOT NULL,
            harga_satuan REAL NOT NULL
        )
        """)

        # Tabel Bahan Baku
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS bahan_baku (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_bahan TEXT NOT NULL,
            stok_pack INTEGER DEFAULT 0,
            berat_per_pack REAL NOT NULL,
            sisa_gram REAL DEFAULT 0,
            batas_min_gram REAL DEFAULT 0
        )
        """)

        # Tabel Penjualan
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS penjualan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT NOT NULL,
            produk_id INTEGER,
            qty INTEGER NOT NULL,
            harga REAL NOT NULL,
            total REAL NOT NULL,
            armada TEXT,
            FOREIGN KEY (produk_id) REFERENCES produk(id)
        )
        """)

        # Tabel Distribusi
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS distribusi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT NOT NULL,
            armada TEXT NOT NULL,
            jumlah_cup INTEGER NOT NULL,
            status TEXT DEFAULT 'terkirim'  -- terkirim / kembali / terjual
        )
        """)

        # Tabel Pemakaian Bahan
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS pemakaian (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT NOT NULL,
            bahan_id INTEGER,
            jumlah_gram REAL NOT NULL,
            sumber_penjualan INTEGER,
            FOREIGN KEY (bahan_id) REFERENCES bahan_baku(id),
            FOREIGN KEY (sumber_penjualan) REFERENCES penjualan(id)
        )
        """)

        self.conn.commit()
        log_debug("Tabel berhasil dibuat atau sudah ada.")

    def tutup(self):
        self.conn.close()
