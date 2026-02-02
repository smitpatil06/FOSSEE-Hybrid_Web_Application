import sys
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QFileDialog, QTableWidget, QTableWidgetItem, 
                             QListWidget, QMessageBox, QFrame, QHeaderView, QSplitter)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

API_URL = "http://127.0.0.1:8000/api"

class ChemicalApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ChemViz - FOSSEE Desktop Client")
        self.setGeometry(100, 100, 1280, 800)
        
        # Set Global Font
        self.setStyleSheet("""
            QMainWindow { background-color: #f5f7fa; }
            QLabel { font-size: 14px; color: #333; }
            QPushButton { 
                background-color: #2563EB; 
                color: white; 
                border-radius: 5px; 
                padding: 8px 15px; 
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #1D4ED8; }
            QListWidget { 
                border: 1px solid #e2e8f0; 
                border-radius: 5px; 
                background-color: white;
                font-size: 13px;
            }
            QTableWidget {
                border: 1px solid #e2e8f0;
                background-color: white;
                gridline-color: #f1f5f9;
                font-size: 12px;
            }
            QHeaderView::section {
                background-color: #f8fafc;
                padding: 4px;
                border: 1px solid #e2e8f0;
                font-weight: bold;
            }
        """)

        # Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # --- Left Sidebar ---
        sidebar_layout = QVBoxLayout()
        
        # Branding Title
        brand_lbl = QLabel("⚗️ ChemViz")
        brand_lbl.setStyleSheet("font-size: 20px; font-weight: bold; color: #1e293b; margin-bottom: 10px;")
        sidebar_layout.addWidget(brand_lbl)

        # Upload Button
        self.btn_upload = QPushButton("Upload New CSV")
        self.btn_upload.setCursor(Qt.PointingHandCursor)
        self.btn_upload.clicked.connect(self.upload_file)
        sidebar_layout.addWidget(self.btn_upload)

        # History List
        sidebar_layout.addWidget(QLabel("Recent Datasets:"))
        self.history_list = QListWidget()
        self.history_list.setCursor(Qt.PointingHandCursor)
        self.history_list.itemClicked.connect(self.load_stats)
        sidebar_layout.addWidget(self.history_list)
        
        # FOSSEE Link
        lbl_fossee = QLabel("Powered by FOSSEE")
        lbl_fossee.setStyleSheet("color: #94a3b8; font-size: 11px; margin-top: 10px;")
        lbl_fossee.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(lbl_fossee)

        # Add sidebar to a container widget
        sidebar_container = QWidget()
        sidebar_container.setLayout(sidebar_layout)
        sidebar_container.setFixedWidth(240)
        sidebar_container.setStyleSheet("background-color: white; border-radius: 10px; border: 1px solid #e2e8f0;")
        main_layout.addWidget(sidebar_container)

        # --- Right Content Area ---
        content_layout = QVBoxLayout()
        
        # 1. Stats Cards Area
        stats_container = QWidget()
        stats_layout = QHBoxLayout(stats_container)
        stats_layout.setContentsMargins(0, 0, 0, 0)
        
        self.card_total = self.create_stat_card("Total Equipment")
        self.card_flow = self.create_stat_card("Avg Flowrate (m³/hr)")
        self.card_press = self.create_stat_card("Avg Pressure (bar)")
        
        stats_layout.addWidget(self.card_total)
        stats_layout.addWidget(self.card_flow)
        stats_layout.addWidget(self.card_press)
        
        content_layout.addWidget(stats_container)

        # 2. Splitter for Chart and Table
        splitter = QSplitter(Qt.Vertical)
        
        # Chart
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.figure.patch.set_facecolor('#f5f7fa') # Match background
        self.canvas = FigureCanvas(self.figure)
        splitter.addWidget(self.canvas)

        # Table
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        splitter.addWidget(self.table)

        content_layout.addWidget(splitter)

        main_layout.addLayout(content_layout)

        # Initial Load
        self.refresh_history()

    def create_stat_card(self, title):
        card = QFrame()
        card.setStyleSheet("background-color: white; border-radius: 8px; border: 1px solid #e2e8f0;")
        layout = QVBoxLayout(card)
        
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #64748b; font-size: 11px; font-weight: bold; text-transform: uppercase;")
        layout.addWidget(lbl_title)
        
        lbl_value = QLabel("-")
        lbl_value.setStyleSheet("color: #0f172a; font-size: 24px; font-weight: bold;")
        lbl_value.setObjectName("value") # Tag for easier finding later
        layout.addWidget(lbl_value)
        
        return card

    def update_card_value(self, card, value):
        # Find the label with objectName 'value' inside the card layout
        for i in range(card.layout().count()):
            widget = card.layout().itemAt(i).widget()
            if widget.objectName() == "value":
                widget.setText(str(value))

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
                QMessageBox.information(self, "Success", "Dataset uploaded successfully!")
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))

    def load_stats(self, item):
        batch_id = item.text().split(' - ')[0]
        try:
            data = requests.get(f"{API_URL}/summary/{batch_id}/").json()
            s = data['summary']

            # Update Cards
            self.update_card_value(self.card_total, s['total_count'])
            self.update_card_value(self.card_flow, f"{s['avg_flow']:.2f}")
            self.update_card_value(self.card_press, f"{s['avg_press']:.2f}")

            # Update Chart
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            dist = data['type_distribution']
            # FOSSEE-like blue color palette
            ax.bar(dist.keys(), dist.values(), color='#3B82F6', alpha=0.7)
            ax.set_title("Equipment Type Distribution", fontsize=10, color='#333')
            ax.tick_params(axis='x', rotation=20, labelsize=8)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            self.figure.tight_layout()
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
            print(f"Error: {e}")

if __name__ == '__main__':
    # Force 'Fusion' style for better look on Linux/Windows
    QApplication.setStyle("Fusion")
    app = QApplication(sys.argv)
    window = ChemicalApp()
    window.show()
    sys.exit(app.exec_())
