from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QFileDialog, QTableWidget, QTableWidgetItem, QMessageBox, 
                             QFrame, QHeaderView, QSplitter, QMenuBar, QAction)
from PyQt5.QtCore import Qt
from ui.components.history_widget import HistoryWidget
from ui.views.charts_widget import ChartsWidget

class UploadWindow(QMainWindow):
    def __init__(self, api_client, user_data, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.user_data = user_data
        self.current_batch_id = None
        
        self.setWindowTitle(f"ChemViz - FOSSEE Desktop Client - {user_data['user']['username']}")
        self.setGeometry(100, 100, 1280, 800)
        
        # Global Styles
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
        
        # Setup Menu Bar
        self.setup_menu_bar()
        
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
        
        # User Info
        user_info = QLabel(f"👤 {user_data['user']['username']}")
        user_info.setStyleSheet("font-size: 12px; color: #64748b; margin-bottom: 15px;")
        sidebar_layout.addWidget(user_info)
        
        # Upload Button
        self.btn_upload = QPushButton("Upload New CSV")
        self.btn_upload.setCursor(Qt.PointingHandCursor)
        self.btn_upload.clicked.connect(self.upload_file)
        sidebar_layout.addWidget(self.btn_upload)
        
        # History Widget
        self.history_widget = HistoryWidget(self.api_client)
        self.history_widget.batch_selected.connect(self.load_batch)
        sidebar_layout.addWidget(self.history_widget)
        
        # FOSSEE Link
        lbl_fossee = QLabel("Powered by FOSSEE")
        lbl_fossee.setStyleSheet("color: #94a3b8; font-size: 11px; margin-top: 10px;")
        lbl_fossee.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(lbl_fossee)
        
        # Sidebar container
        sidebar_container = QWidget()
        sidebar_container.setLayout(sidebar_layout)
        sidebar_container.setFixedWidth(260)
        sidebar_container.setStyleSheet("background-color: white; border-radius: 10px; border: 1px solid #e2e8f0;")
        main_layout.addWidget(sidebar_container)
        
        # --- Right Content Area ---
        content_layout = QVBoxLayout()
        
        # Stats Cards
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
        
        # Splitter for Chart and Table
        splitter = QSplitter(Qt.Vertical)
        
        # Chart Widget
        self.chart_widget = ChartsWidget()
        splitter.addWidget(self.chart_widget)
        
        # Table
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        splitter.addWidget(self.table)
        
        content_layout.addWidget(splitter)
        main_layout.addLayout(content_layout)
        
        # Load initial data
        self.history_widget.refresh()
    
    def setup_menu_bar(self):
        """Setup menu bar"""
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu('File')
        
        upload_action = QAction('Upload CSV', self)
        upload_action.triggered.connect(self.upload_file)
        file_menu.addAction(upload_action)
        
        file_menu.addSeparator()
        
        logout_action = QAction('Logout', self)
        logout_action.triggered.connect(self.logout)
        file_menu.addAction(logout_action)
        
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Help Menu
        help_menu = menubar.addMenu('Help')
        
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_stat_card(self, title):
        """Create a stat card widget"""
        card = QFrame()
        card.setStyleSheet("background-color: white; border-radius: 8px; border: 1px solid #e2e8f0;")
        layout = QVBoxLayout(card)
        
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #64748b; font-size: 11px; font-weight: bold; text-transform: uppercase;")
        layout.addWidget(lbl_title)
        
        lbl_value = QLabel("-")
        lbl_value.setStyleSheet("color: #0f172a; font-size: 24px; font-weight: bold;")
        lbl_value.setObjectName("value")
        layout.addWidget(lbl_value)
        
        return card
    
    def update_card_value(self, card, value):
        """Update stat card value"""
        for i in range(card.layout().count()):
            widget = card.layout().itemAt(i).widget()
            if widget.objectName() == "value":
                widget.setText(str(value))
    
    def upload_file(self):
        """Handle file upload"""
        fname, _ = QFileDialog.getOpenFileName(self, 'Open CSV', '.', 'CSV Files (*.csv)')
        if fname:
            try:
                self.api_client.upload_file(fname)
                self.history_widget.refresh()
                QMessageBox.information(self, "Success", "Dataset uploaded successfully!")
            except Exception as e:
                error_msg = str(e)
                if hasattr(e, 'response') and e.response is not None:
                    try:
                        error_data = e.response.json()
                        error_msg = error_data.get('error', error_msg)
                    except:
                        pass
                QMessageBox.warning(self, "Error", f"Upload failed: {error_msg}")
    
    def load_batch(self, batch_id):
        """Load batch data"""
        self.current_batch_id = batch_id
        try:
            data = self.api_client.get_summary(batch_id)
            summary = data['summary']
            
            # Update Cards
            self.update_card_value(self.card_total, summary['total_count'])
            self.update_card_value(self.card_flow, f"{summary['avg_flow']:.2f}")
            self.update_card_value(self.card_press, f"{summary['avg_press']:.2f}")
            
            # Update Chart
            self.chart_widget.update_chart(data['type_distribution'])
            
            # Update Table
            rows = data['data']
            self.table.setRowCount(len(rows))
            self.table.setColumnCount(5)
            self.table.setHorizontalHeaderLabels(['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'])
            
            for i, row in enumerate(rows):
                self.table.setItem(i, 0, QTableWidgetItem(str(row['equipment_name'])))
                self.table.setItem(i, 1, QTableWidgetItem(str(row['equipment_type'])))
                self.table.setItem(i, 2, QTableWidgetItem(str(row['flowrate'])))
                self.table.setItem(i, 3, QTableWidgetItem(str(row['pressure'])))
                self.table.setItem(i, 4, QTableWidgetItem(str(row['temperature'])))
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load data: {str(e)}")
    
    def logout(self):
        """Handle logout"""
        reply = QMessageBox.question(self, 'Logout', 'Are you sure you want to logout?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.api_client.logout()
            self.close()
            # The main.py will handle showing login window again
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "About ChemViz",
                         "ChemViz - Chemical Data Visualization Platform\n\n"
                         "Developed for FOSSEE Screening Task\n\n"
                         "Features:\n"
                         "• CSV data upload and analysis\n"
                         "• Equipment parameter visualization\n"
                         "• PDF report generation\n"
                         "• Multi-user authentication\n\n"
                         "Powered by FOSSEE")
