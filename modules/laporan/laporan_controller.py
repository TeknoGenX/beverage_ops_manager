# modules/laporan/laporan_controller.py

import csv
from fpdf import FPDF
from PyQt5.QtWidgets import QFileDialog, QMessageBox

class LaporanController:
    def export_to_excel(self, headers, data, parent):
        path, _ = QFileDialog.getSaveFileName(parent, "Simpan Excel", "", "CSV File (*.csv)")
        if path:
            with open(path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(data)
            QMessageBox.information(parent, "Berhasil", "Laporan berhasil disimpan sebagai CSV.")

    def export_to_pdf(self, title, headers, data, parent):
        path, _ = QFileDialog.getSaveFileName(parent, "Simpan PDF", "", "PDF File (*.pdf)")
        if path:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(200, 10, title, ln=True, align='C')
            pdf.ln(10)

            pdf.set_font("Arial", '', 10)
            col_width = 190 / len(headers)
            for header in headers:
                pdf.cell(col_width, 10, header, border=1)
            pdf.ln()

            for row in data:
                for item in row:
                    pdf.cell(col_width, 10, str(item), border=1)
                pdf.ln()

            pdf.output(path)
            QMessageBox.information(parent, "Berhasil", "Laporan berhasil disimpan sebagai PDF.")
