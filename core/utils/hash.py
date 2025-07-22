# core/utils/hash.py

import bcrypt

def hash_password(password: str) -> str:
    """
    Mengubah password plain-text menjadi hash menggunakan bcrypt.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()

def cek_password(password: str, hashed: str) -> bool:
    """
    Membandingkan password input dengan hash yang tersimpan.
    """
    try:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    except Exception:
        return False
