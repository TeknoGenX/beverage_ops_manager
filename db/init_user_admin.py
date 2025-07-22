import bcrypt
from db.models import Database
from config import log_debug

def tambah_admin_default():
    db = Database()

    # Cek apakah user admin sudah ada
    db.cursor.execute("SELECT * FROM users WHERE username = ?", ('admin',))
    existing = db.cursor.fetchone()

    if existing:
        log_debug("User admin sudah ada, tidak perlu dibuat ulang.")
    else:
        password = "admin123"
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        db.cursor.execute("""
            INSERT INTO users (username, password_hash, role)
            VALUES (?, ?, ?)
        """, ('admin', hashed, 'admin'))

        db.conn.commit()
        log_debug("User admin berhasil ditambahkan (username: admin, password: admin123)")

    db.tutup()

if __name__ == "__main__":
    tambah_admin_default()
