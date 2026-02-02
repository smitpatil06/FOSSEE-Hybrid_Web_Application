from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QListWidgetItem, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal

class HistoryWidget(QWidget):
    batch_selected = pyqtSignal(int)  # Signal emits batch_id
    batch_deleted = pyqtSignal()  # Signal when batch is deleted
    
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        
        # Title with refresh button
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(5)
        
        title = QLabel("Recent Datasets:")
        title.setStyleSheet("font-weight: bold; font-size: 12px; color: #64748b;")
        title_layout.addWidget(title)
        title_layout.addStretch()
        
        refresh_btn = QPushButton("↻")
        refresh_btn.setFixedSize(22, 22)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #e2e8f0;
                color: #1e293b;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                padding: 0px;
                font-size: 11px;
            }
            QPushButton:hover { background-color: #cbd5e1; }
        """)
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.clicked.connect(self.refresh)
        title_layout.addWidget(refresh_btn)
        layout.addLayout(title_layout)
        
        # List Widget
        self.list_widget = QListWidget()
        self.list_widget.setCursor(Qt.PointingHandCursor)
        self.list_widget.setStyleSheet("""
            QListWidget {
                border: 1px solid #e2e8f0; 
                border-radius: 5px; 
                background-color: white;
                font-size: 12px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f1f5f9;
            }
            QListWidget::item:selected {
                background-color: #dbeafe;
                color: #1e40af;
            }
            QListWidget::item:hover {
                background-color: #f1f5f9;
            }
        """)
        self.list_widget.itemClicked.connect(self.on_item_clicked)
        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.on_right_click)
        layout.addWidget(self.list_widget)
        
        # Delete instructions label
        help_label = QLabel("Right-click to delete dataset")
        help_label.setStyleSheet("font-size: 10px; color: #94a3b8; italic; margin-top: 5px;")
        help_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(help_label)
        
        self.setLayout(layout)
    
    def refresh(self):
        """Refresh history list from API"""
        try:
            history = self.api_client.get_history()
            self.list_widget.clear()
            
            for item in history:
                batch_id = item['id']
                filename = item['filename']
                uploaded_at = item['uploaded_at']
                uploaded_by = item.get('uploaded_by', {}).get('username', 'Unknown')
                
                # Create list item with batch_id as data
                list_item = QListWidgetItem(f"📊 {filename}")
                list_item.setData(Qt.UserRole, batch_id)
                list_item.setToolTip(f"Uploaded by: {uploaded_by}\n{uploaded_at}\n\nRight-click to delete")
                self.list_widget.addItem(list_item)
            
            # Auto-select first item if available
            if self.list_widget.count() > 0:
                self.list_widget.setCurrentRow(0)
                first_item = self.list_widget.item(0)
                batch_id = first_item.data(Qt.UserRole)
                self.batch_selected.emit(batch_id)
                
        except Exception as e:
            print(f"Error refreshing history: {e}")
    
    def on_item_clicked(self, item):
        """Handle item click"""
        batch_id = item.data(Qt.UserRole)
        self.batch_selected.emit(batch_id)
    
    def on_right_click(self, pos):
        """Handle right-click for delete option"""
        item = self.list_widget.itemAt(pos)
        if item:
            batch_id = item.data(Qt.UserRole)
            filename = item.text().replace("📊 ", "")
            
            reply = QMessageBox.question(
                self,
                "Delete Dataset",
                f"Delete '{filename}'?\nThis action cannot be undone.",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.delete_batch(batch_id)
    
    def delete_batch(self, batch_id):
        """Delete a batch from history"""
        try:
            response = self.api_client.session.delete(
                f"{self.api_client.base_url}/summary/{batch_id}/"
            )
            if response.status_code in [200, 204, 404]:
                QMessageBox.information(self, "Success", "Dataset deleted successfully!")
                self.batch_deleted.emit()
                self.refresh()
            else:
                QMessageBox.warning(self, "Error", f"Failed to delete dataset: {response.status_code}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to delete: {str(e)}")
