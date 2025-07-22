# modules/grafik/grafik_controller.py

from .grafik_model.py import GrafikModel

class GrafikController:
    def __init__(self):
        self.model = GrafikModel()

    def get_penjualan_per_produk(self, tanggal_mulai=None, tanggal_akhir=None):
        return self.model.penjualan_per_produk(tanggal_mulai, tanggal_akhir)

    def get_pemakaian_bahan_per_bulan(self):
        return self.model.pemakaian_bahan_per_bulan()

    def get_armada_terbaik(self):
        return self.model.armada_terbaik()
