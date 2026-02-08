from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QListWidgetItem, QMessageBox, QToolButton, QStyle
from PyQt5.QtCore import Qt, pyqtSignal

class HistoryWidget(QWidget):
    batch_selected = pyqtSignal(int)  # Signal emits batch_id
    batch_deleted = pyqtSignal(int)  # Signal when batch is deleted; emits deleted batch_id
    batch_deleted_simple = pyqtSignal()  # Backwards-compatible no-arg delete signal
    
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
                border-radius: 6px; 
                background-color: #ffffff;
                font-size: 12px;
            }
            QListWidget::item {
                padding: 6px;
                border-bottom: 1px solid #f1f5f9;
            }
            QListWidget::item:selected {
                background-color: #e0f2fe;
                color: #0f172a;
            }
            QListWidget::item:hover {
                background-color: #f8fafc;
            }
        """)
        self.list_widget.itemClicked.connect(self.on_item_clicked)
        layout.addWidget(self.list_widget)
        
        # Delete instructions label
        help_label = QLabel("Click trash icon to delete")
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

                # Create list item container widget (filename + delete icon)
                container = QWidget()
                container_layout = QHBoxLayout(container)
                container_layout.setContentsMargins(8, 6, 8, 6)
                container_layout.setSpacing(8)

                label = QLabel(filename)
                label.setStyleSheet("font-size: 12px; font-weight: 600; color: #0f172a;")
                label.setWordWrap(True)

                meta = QLabel(f"{uploaded_at} • {uploaded_by}")
                meta.setStyleSheet("font-size: 10px; color: #64748b;")

                text_box = QWidget()
                text_layout = QVBoxLayout(text_box)
                text_layout.setContentsMargins(0, 0, 0, 0)
                text_layout.setSpacing(2)
                text_layout.addWidget(label)
                text_layout.addWidget(meta)

                del_btn = QToolButton()
                del_btn.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
                del_btn.setToolTip("Delete dataset")
                del_btn.setFixedSize(26, 26)
                del_btn.setStyleSheet(
                    "QToolButton { background-color: #fee2e2; color: #b91c1c; border: 1px solid #fecaca; border-radius: 4px; }"
                    "QToolButton:hover { background-color: #fecaca; }"
                )
                del_btn.setCursor(Qt.PointingHandCursor)
                del_btn.clicked.connect(lambda _, b=batch_id, f=filename: self._confirm_and_delete(b, f))

                container_layout.addWidget(text_box)
                container_layout.addStretch()
                container_layout.addWidget(del_btn)

                list_item = QListWidgetItem()
                list_item.setData(Qt.UserRole, batch_id)
                list_item.setSizeHint(container.sizeHint())
                self.list_widget.addItem(list_item)
                self.list_widget.setItemWidget(list_item, container)
            
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
    
    def _confirm_and_delete(self, batch_id, filename):
        """Helper connected to visible Delete buttons"""
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
                # Emit deleted batch id so parent can clear selection if it was selected
                self.batch_deleted.emit(batch_id)
                # Also emit simple no-arg signal for backwards compatibility
                self.batch_deleted_simple.emit()
                # Remove the specific item from the list to update UI immediately
                for i in range(self.list_widget.count()):
                    it = self.list_widget.item(i)
                    if it.data(Qt.UserRole) == batch_id:
                        self.list_widget.takeItem(i)
                        break
                # Refresh to ensure consistent state
                self.refresh()
            else:
                QMessageBox.warning(self, "Error", f"Failed to delete dataset: {response.status_code}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to delete: {str(e)}")
