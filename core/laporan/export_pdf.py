# core/laporan/export_pdf.py

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os

from config import log_debug

class PDFExporter:
    def __init__(self, judul="Laporan", output_dir="exports"):
        self.judul = judul
        self.output_dir = output_dir

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            log_debug(f"Folder '{self.output_dir}' dibuat.")

    def buat_pdf(self, nama_file: str, data: list, kolom: list) -> str:
        """
        nama_file: nama file tanpa .pdf
        data: list of tuple/dict berisi data baris
        kolom: list nama kolom sebagai header tabel
        return: path lengkap file PDF
        """

        path_file = os.path.join(self.output_dir, f"{nama_file}.pdf")
        log_debug(f"Membuat PDF di: {path_file}")

        c = canvas.Canvas(path_file, pagesize=A4)
        lebar, tinggi = A4

        # Header
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(lebar / 2, tinggi - 50, self.judul)

        # Tanggal
        c.setFont("Helvetica", 10)
        c.drawString(40, tinggi - 70, f"Dibuat: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")

        # Table Header
        y = tinggi - 100
        x = 40
        kolom_width = 500 // len(kolom)

        c.setFont("Helvetica-Bold", 10)
        for i, nama in enumerate(kolom):
            c.drawString(x + i * kolom_width, y, str(nama))

        # Data Baris
        c.setFont("Helvetica", 10)
        y -= 20
        for baris in data:
            if y < 50:
                c.showPage()
                y = tinggi - 50

            for i, kol in enumerate(kolom):
                nilai = baris.get(kol, "") if isinstance(baris, dict) else baris[i]
                c.drawString(x + i * kolom_width, y, str(nilai))
            y -= 15

        c.save()
        log_debug(f"PDF selesai dibuat: {path_file}")
        return path_file
