import bcrypt
import sqlite3
import os

# Konfigurasi
DB_PATH = "db/beverage_ops.db"
USERNAME = "admin"
PASSWORD = "admin123"
ROLE = "admin"

# Buat hash password
password_hash = bcrypt.hashpw(PASSWORD.encode(), bcrypt.gensalt()).decode()

# Pastikan database ada
if not os.path.exists(DB_PATH):
    print(f"[ERROR] Database tidak ditemukan: {DB_PATH}")
    exit()

# Hubungkan ke database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Pastikan tabel users ada
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL
)
""")

# Cek apakah username sudah ada
cursor.execute("SELECT * FROM users WHERE username = ?", (USERNAME,))
if cursor.fetchone():
    print(f"[INFO] Username '{USERNAME}' sudah terdaftar.")
else:
    # Insert user baru
    cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                   (USERNAME, password_hash, ROLE))
    conn.commit()
    print(f"[SUCCESS] User '{USERNAME}' berhasil dibuat.")

conn.close()
