# modules/grafik/grafik_view.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from .grafik_controller import GrafikController

class GrafikView(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = GrafikController()
        self.setWindowTitle("Grafik Penjualan & Pemakaian")
        self.setMinimumSize(800, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Inisialisasi grafik
        self.canvas = FigureCanvas(Figure(figsize=(8, 5)))
        self.ax = self.canvas.figure.add_subplot(111)

        self.layout.addWidget(self.canvas)

        # Tampilkan grafik awal
        self.tampilkan_grafik_penjualan_per_produk()

    def tampilkan_grafik_penjualan_per_produk(self):
        data = self.controller.get_penjualan_per_produk()
        if not data:
            self.ax.clear()
            self.ax.text(0.5, 0.5, "Data kosong", ha='center', va='center')
        else:
            produk, total = zip(*data)
            self.ax.clear()
            self.ax.bar(produk, total, color='skyblue')
            self.ax.set_title("Penjualan per Produk")
            self.ax.set_ylabel("Jumlah Terjual")
            self.ax.set_xticklabels(produk, rotation=45, ha='right')

        self.canvas.draw()

    def tampilkan_grafik_pemakaian_bahan(self):
        data = self.controller.get_pemakaian_bahan_per_bulan()
        if not data:
            self.ax.clear()
            self.ax.text(0.5, 0.5, "Data kosong", ha='center', va='center')
        else:
            bulan, total = zip(*data)
            self.ax.clear()
            self.ax.plot(bulan, total, marker='o', color='green')
            self.ax.set_title("Pemakaian Bahan per Bulan")
            self.ax.set_ylabel("Jumlah (gram)")
            self.ax.set_xticklabels(bulan, rotation=45, ha='right')

        self.canvas.draw()
