import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QMessageBox

API_URL = "http://localhost:5000/rekap"

class RekapApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rekap Distribusi")
        self.layout = QVBoxLayout()
        self.list_widget = QListWidget()
        self.refresh_button = QPushButton("Refresh Rekap List")
        self.refresh_button.clicked.connect(self.load_rekap)
        self.layout.addWidget(self.refresh_button)
        self.layout.addWidget(self.list_widget)
        self.setLayout(self.layout)
        self.load_rekap()

    def load_rekap(self):
        self.list_widget.clear()
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                # You need to adjust this depending on your API's response format
                # If /rekap returns HTML, you need to create a JSON endpoint
                # For demonstration, let's assume you have a /rekap/json endpoint
                data = requests.get(API_URL + "/json").json()
                for item in data:
                    self.list_widget.addItem(f"{item['id']}: {item['tanggal']} - {item['jumlah']} - {item['keterangan']}")
            else:
                QMessageBox.warning(self, "Error", "Failed to fetch data")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RekapApp()
    window.show()
    sys.exit(app.exec_())
