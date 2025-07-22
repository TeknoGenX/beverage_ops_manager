# core/dashboard/dashboard_view.py

from PyQt5.QtWidgets import QMessageBox
from config import log_debug

class DashboardView:
    def __init__(self, controller):
        """
        controller: instance dari DashboardController (QMainWindow)
        """
        self.controller = controller

    def tampilkan_admin_panel(self):
        log_debug("Menampilkan dashboard admin")
        self._aktifkan_semua_menu()

    def tampilkan_supervisor_panel(self):
        log_debug("Menampilkan dashboard supervisor")
        self._nonaktifkan_menu(["menuManajemenUser"])
        self._aktifkan_menu(["menuLaporan", "menuProduk", "menuStok"])

    def tampilkan_kasir_panel(self):
        log_debug("Menampilkan dashboard kasir")
        self._nonaktifkan_menu(["menuManajemenUser", "menuStok", "menuLaporan"])
        self._aktifkan_menu(["menuTransaksi", "menuProduk"])

    def tampilkan_gudang_panel(self):
        log_debug("Menampilkan dashboard staff gudang")
        self._nonaktifkan_menu(["menuManajemenUser", "menuTransaksi", "menuLaporan"])
        self._aktifkan_menu(["menuStok"])

    def _aktifkan_menu(self, daftar_menu):
        for nama in daftar_menu:
            item = getattr(self.controller, nama, None)
            if item:
                item.setEnabled(True)
            else:
                log_debug(f"[WARNING] Menu '{nama}' tidak ditemukan di UI.")

    def _nonaktifkan_menu(self, daftar_menu):
        for nama in daftar_menu:
            item = getattr(self.controller, nama, None)
            if item:
                item.setEnabled(False)
            else:
                log_debug(f"[WARNING] Menu '{nama}' tidak ditemukan di UI.")

    def _aktifkan_semua_menu(self):
        # Asumsikan ini adalah semua nama menu yang ada
        semua_menu = [
            "menuManajemenUser", "menuTransaksi", "menuProduk",
            "menuStok", "menuLaporan"
        ]
        self._aktifkan_menu(semua_menu)
