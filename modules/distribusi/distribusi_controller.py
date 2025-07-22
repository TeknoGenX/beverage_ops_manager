# modules/distribusi/distribusi_controller.py

from modules.distribusi.distribusi_model import DistribusiModel

class DistribusiController:
    def __init__(self, view):
        self.view = view
        self.model = DistribusiModel()
        self.load_data()

    def load_data(self):
        data = self.model.get_semua_distribusi()
        self.view.tampilkan_data_distribusi(data)

    def tambah_distribusi(self, tanggal, armada, jumlah_cup, status):
        if not tanggal or not armada or not jumlah_cup:
            self.view.tampilkan_pesan("Semua field harus diisi.")
            return

        try:
            jumlah = int(jumlah_cup)
        except ValueError:
            self.view.tampilkan_pesan("Jumlah cup harus berupa angka.")
            return

        self.model.tambah_distribusi(tanggal, armada, jumlah, status)
        self.view.tampilkan_pesan("Distribusi berhasil ditambahkan.")
        self.load_data()

    def hapus_distribusi(self, distribusi_id):
        self.model.hapus_distribusi(distribusi_id)
        self.view.tampilkan_pesan("Distribusi berhasil dihapus.")
        self.load_data()
