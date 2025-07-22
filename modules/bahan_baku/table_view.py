# File: modules/bahan_baku/table_view.py
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant
from PyQt5.QtWidgets import QApplication
import sys

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableView, QPushButton, QHBoxLayout, QMessageBox
)

class BahanBakuTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()
        self.header = ["ID", "Nama", "Stok", "Satuan", "Harga"]
        self._data = data or []

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self.header)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()
        if role == Qt.DisplayRole:
            return str(self._data[index.row()][index.column()])
        return QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.header[section]
            else:
                return str(section + 1)
        return QVariant()

    def addRow(self, row_data):
        self.beginInsertRows(QVariant(), self.rowCount(), self.rowCount())
        self._data.append(row_data)
        self.endInsertRows()

    def removeRow(self, row):
        if 0 <= row < self.rowCount():
            self.beginRemoveRows(QVariant(), row, row)
            del self._data[row]
            self.endRemoveRows()

class BahanBakuTableView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Daftar Bahan Baku")
        self.resize(700, 400)

        self.model = BahanBakuTableModel([
            [1, "Gula", 100, "kg", 12000],
            [2, "Kopi", 50, "kg", 80000],
            [3, "Susu", 30, "liter", 15000],
        ])

        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSelectionMode(QTableView.SingleSelection)

        self.add_btn = QPushButton("Tambah")
        self.delete_btn = QPushButton("Hapus")

        self.add_btn.clicked.connect(self.add_row)
        self.delete_btn.clicked.connect(self.delete_row)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addStretch()

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def add_row(self):
        # Dummy data, replace with dialog/form as needed
        next_id = self.model.rowCount() + 1
        self.model.addRow([next_id, "Bahan Baru", 0, "unit", 0])

    def delete_row(self):
        selected = self.table.selectionModel().selectedRows()
        if selected:
            row = selected[0].row()
            confirm = QMessageBox.question(
                self, "Konfirmasi", "Hapus baris terpilih?",
                QMessageBox.Yes | QMessageBox.No
            )
            if confirm == QMessageBox.Yes:
                self.model.removeRow(row)
        else:
            QMessageBox.warning(self, "Peringatan", "Pilih baris yang akan dihapus.")

# For testing standalone
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BahanBakuTableView()
    window.show()
    sys.exit(app.exec_())