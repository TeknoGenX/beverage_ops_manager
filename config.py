# config.py

import os

# =======================
# 🧠 Konfigurasi Umum
# =======================
NAMA_APLIKASI = "BeverageOps Manager"
VERSI = "1.0.0"
DEVELOPER = "Tim BeverageOps"
LOKASI_LOGO = os.path.join("assets", "logo.png")
MODE_DEBUG = True

# ==========================
# 🗃️ Konfigurasi Database
# ==========================
NAMA_DATABASE = "beverage_ops.db"
PATH_DATABASE = os.path.join("db", NAMA_DATABASE)

# =============================
# 🎨 Pengaturan Tampilan UI
# =============================
MODE_TEMA = "dark"

# =============================
# 🔐 Hak Akses & Role
# =============================
ROLE = {
    "admin": "Administrator",
    "supervisor": "Supervisor",
    "kasir": "Kasir",
    "staff": "Staff Gudang"
}

# ============================
# 📎 File Laporan & Export
# ============================
FOLDER_LAPORAN = os.path.join("exports")
EXT_PDF = ".pdf"
EXT_EXCEL = ".xlsx"

# ============================
# 📝 Logging
# ============================
FOLDER_LOG = "logs"
LOG_FILE = "app.log"
LOG_FILE_PATH = os.path.join(FOLDER_LOG, LOG_FILE)

# ============================
# 🛠 Fungsi Bantuan
# ============================
def log_debug(pesan):
    """Tampilkan log debug jika MODE_DEBUG diaktifkan"""
    if MODE_DEBUG:
        print(f"[DEBUG] {pesan}")
        try:
            with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
                f.write(f"[DEBUG] {pesan}\n")
        except Exception as e:
            print("[ERROR] Tidak bisa menulis ke file log:", e)

# ============================
# 📁 Inisialisasi Folder Wajib
# ============================
def init_folders():
    for folder in ["assets", "db", FOLDER_LAPORAN, FOLDER_LOG]:
        if not os.path.exists(folder):
            os.makedirs(folder)
            log_debug(f"Membuat folder: {folder}")
