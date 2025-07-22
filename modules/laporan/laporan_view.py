# modules/laporan/laporan_view.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QDateEdit, QLabel, QHBoxLayout
from datetime import datetime
from modules.laporan.laporan_model import LaporanModel
from modules.laporan.laporan_controller import LaporanController

class LaporanView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Laporan Penjualan & Distribusi")
        self.model = LaporanModel()
        self.controller = LaporanController()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        tanggal_layout = QHBoxLayout()
        self.tgl_awal = QDateEdit()
        self.tgl_akhir = QDateEdit()
        self.tgl_awal.setCalendarPopup(True)
        self.tgl_akhir.setCalendarPopup(True)

        tanggal_layout.addWidget(QLabel("Dari:"))
        tanggal_layout.addWidget(self.tgl_awal)
        tanggal_layout.addWidget(QLabel("Sampai:"))
        tanggal_layout.addWidget(self.tgl_akhir)

        self.btn_export_csv = QPushButton("Export ke Excel (CSV)")
        self.btn_export_pdf = QPushButton("Export ke PDF")

        self.btn_export_csv.clicked.connect(self.export_csv)
        self.btn_export_pdf.clicked.connect(self.export_pdf)

        layout.addLayout(tanggal_layout)
        layout.addWidget(self.btn_export_csv)
        layout.addWidget(self.btn_export_pdf)

        self.setLayout(layout)

    def export_csv(self):
        data = self.model.get_laporan_penjualan(self.tgl_awal.date().toString("yyyy-MM-dd"),
                                                 self.tgl_akhir.date().toString("yyyy-MM-dd"))
        headers = ["Tanggal", "Produk", "Qty", "Harga", "Total", "Armada"]
        self.controller.export_to_excel(headers, data, self)

    def export_pdf(self):
        data = self.model.get_laporan_penjualan(self.tgl_awal.date().toString("yyyy-MM-dd"),
                                                 self.tgl_akhir.date().toString("yyyy-MM-dd"))
        headers = ["Tanggal", "Produk", "Qty", "Harga", "Total", "Armada"]
        self.controller.export_to_pdf("Laporan Penjualan", headers, data, self)
