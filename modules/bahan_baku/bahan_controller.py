# modules/bahan_baku/bahan_controller.py

from PyQt5.QtWidgets import QMessageBox
from modules.bahan_baku.bahan_model import BahanModel

class BahanController:
    def __init__(self, view):
        self.view = view
        self.model = BahanModel()
        self.load_data()

    def load_data(self):
        self.view.tabel.setRowCount(0)
        data = self.model.semua()
        for row_data in data:
            self.view.tambah_ke_tabel(row_data)

    def simpan(self):
        if not self.view.validasi_input():
            return

        data = self.view.get_input_data()
        if self.view.editing_id is None:
            self.model.tambah(*data)
            QMessageBox.information(self.view, "Sukses", "Bahan baku berhasil ditambahkan.")
        else:
            self.model.ubah(self.view.editing_id, *data)
            QMessageBox.information(self.view, "Sukses", "Bahan baku berhasil diperbarui.")

        self.view.clear_input()
        self.view.editing_id = None
        self.load_data()

    def hapus(self):
        id_bahan = self.view.get_selected_id()
        if id_bahan:
            confirm = QMessageBox.question(
                self.view, "Konfirmasi", "Yakin ingin menghapus data ini?",
                QMessageBox.Yes | QMessageBox.No
            )
            if confirm == QMessageBox.Yes:
                self.model.hapus(id_bahan)
                self.load_data()
                self.view.clear_input()

    def muat_untuk_edit(self):
        id_bahan = self.view.get_selected_id()
        if id_bahan:
            data = self.model.cari_by_id(id_bahan)
            if data:
                self.view.set_input_data(data)
                self.view.editing_id = id_bahan
