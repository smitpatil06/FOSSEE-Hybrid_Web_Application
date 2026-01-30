import sys
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QFileDialog, QTableWidget, QTableWidgetItem, 
                             QListWidget, QMessageBox, QFrame)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

API_URL = "http://127.0.0.1:8000/api"

class ChemicalApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Visualizer (Desktop)")
        self.setGeometry(100, 100, 1200, 700)
        
        main_layout = QHBoxLayout()
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # --- Sidebar ---
        sidebar = QVBoxLayout()
        self.btn_upload = QPushButton("Upload CSV")
        self.btn_upload.setStyleSheet("background-color: #2196F3; color: white; padding: 10px; font-weight: bold;")
        self.btn_upload.clicked.connect(self.upload_file)
        sidebar.addWidget(self.btn_upload)
        
        sidebar.addWidget(QLabel("<b>History:</b>"))
        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.load_stats)
        sidebar.addWidget(self.history_list)
        
        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar)
        sidebar_widget.setFixedWidth(200)
        main_layout.addWidget(sidebar_widget)

        # --- Content ---
        content = QVBoxLayout()
        
        # Stats
        stats_box = QHBoxLayout()
        self.lbl_total = QLabel("Total: -")
        self.lbl_flow = QLabel("Avg Flow: -")
        self.lbl_press = QLabel("Avg Press: -")
        for l in [self.lbl_total, self.lbl_flow, self.lbl_press]:
            l.setStyleSheet("border: 1px solid #ddd; padding: 15px; font-size: 14px; background: #f9f9f9; border-radius: 5px;")
            stats_box.addWidget(l)
        content.addLayout(stats_box)

        # Chart
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        content.addWidget(self.canvas)

        # Table
        self.table = QTableWidget()
        content.addWidget(self.table)

        content_widget = QWidget()
        content_widget.setLayout(content)
        main_layout.addWidget(content_widget)

        self.refresh_history()

    def refresh_history(self):
        try:
            res = requests.get(f"{API_URL}/history/")
            self.history_list.clear()
            for item in res.json():
                self.history_list.addItem(f"{item['id']} - {item['filename']}")
        except: pass

    def upload_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open CSV', '.', 'CSV Files (*.csv)')
        if fname:
            try:
                files = {'file': open(fname, 'rb')}
                requests.post(f"{API_URL}/upload/", files=files)
                self.refresh_history()
                QMessageBox.information(self, "Success", "File Uploaded!")
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))

    def load_stats(self, item):
        batch_id = item.text().split(' - ')[0]
        try:
            data = requests.get(f"{API_URL}/summary/{batch_id}/").json()
            
            # Update Labels
            s = data['summary']
            self.lbl_total.setText(f"Total: {s['total_count']}")
            self.lbl_flow.setText(f"Avg Flow: {s['avg_flow']:.1f}")
            self.lbl_press.setText(f"Avg Press: {s['avg_press']:.1f}")

            # Update Chart
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            dist = data['type_distribution']
            ax.bar(dist.keys(), dist.values(), color='#4CAF50')
            ax.set_title("Equipment Distribution")
            self.canvas.draw()

            # Update Table
            rows = data['data']
            self.table.setRowCount(len(rows))
            self.table.setColumnCount(5)
            self.table.setHorizontalHeaderLabels(['Name', 'Type', 'Flow', 'Press', 'Temp'])
            for i, row in enumerate(rows):
                self.table.setItem(i, 0, QTableWidgetItem(str(row['equipment_name'])))
                self.table.setItem(i, 1, QTableWidgetItem(str(row['equipment_type'])))
                self.table.setItem(i, 2, QTableWidgetItem(str(row['flowrate'])))
                self.table.setItem(i, 3, QTableWidgetItem(str(row['pressure'])))
                self.table.setItem(i, 4, QTableWidgetItem(str(row['temperature'])))
        except Exception as e:
            print(e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChemicalApp()
    window.show()
    sys.exit(app.exec_())