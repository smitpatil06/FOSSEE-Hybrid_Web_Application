import json
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QAction,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QGridLayout,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QHeaderView,
)
from PyQt5.QtCore import QSettings
from ui.components.history_widget import HistoryWidget
from ui.views.charts_widget import ChartWidget


class UploadWindow(QMainWindow):
    def __init__(self, api_client, user_data, parent=None):
        super().__init__(parent)
        self.settings = QSettings("ChemLabWizard", "DesktopClient")
        self.api_client = api_client
        self.user_data = user_data
        self.current_batch_id = None
        self.current_rows = []
        self.current_distribution = {}
        self.chart_widgets = []

        self.setWindowTitle(
            f"ChemLabWizard - BI Dashboard - {user_data['user']['username']}"
        )
        self.setGeometry(80, 60, 1400, 860)
        self.setFont(QFont("Segoe UI", 10))

        self.setStyleSheet(
            ""
            "QMainWindow { background-color: #f8fafc; }"
            "QLabel { color: #1f2937; }"
            "QPushButton {"
            "  background-color: #2563eb; color: white; border-radius: 6px;"
            "  padding: 8px 16px; font-weight: 600;"
            "}"
            "QPushButton:hover { background-color: #1d4ed8; }"
            "QTableWidget { background-color: #ffffff; color: #111827;"
            "  border: 1px solid #e2e8f0; gridline-color: #e2e8f0; }"
            "QHeaderView::section { background-color: #f1f5f9; color: #111827;"
            "  padding: 6px; border: 1px solid #e2e8f0; font-weight: 600; }"
        )

        self.setup_menu_bar()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)

        sidebar_layout = QVBoxLayout()
        brand_lbl = QLabel("⚗️ ChemLabWizard")
        brand_lbl.setStyleSheet("font-size: 20px; font-weight: 700; color: #0f172a;")
        sidebar_layout.addWidget(brand_lbl)

        user_info = QLabel(f"👤 {user_data['user']['username']}")
        user_info.setStyleSheet("font-size: 12px; color: #64748b; margin-bottom: 12px;")
        sidebar_layout.addWidget(user_info)

        self.btn_upload = QPushButton("Upload CSV")
        self.btn_upload.setCursor(Qt.PointingHandCursor)
        self.btn_upload.clicked.connect(self.upload_file)
        sidebar_layout.addWidget(self.btn_upload)

        self.history_widget = HistoryWidget(self.api_client)
        self.history_widget.batch_selected.connect(self.load_batch)
        try:
            self.history_widget.batch_deleted.connect(self.on_batch_deleted)
        except Exception:
            self.history_widget.batch_deleted_simple.connect(lambda: self.on_batch_deleted(None))
        sidebar_layout.addWidget(self.history_widget)

        lbl_fossee = QLabel("Powered by FOSSEE")
        lbl_fossee.setStyleSheet("color: #94a3b8; font-size: 11px; margin-top: 10px;")
        lbl_fossee.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(lbl_fossee)

        sidebar_container = QWidget()
        sidebar_container.setLayout(sidebar_layout)
        sidebar_container.setFixedWidth(280)
        sidebar_container.setStyleSheet(
            "background-color: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0;"
        )
        main_layout.addWidget(sidebar_container)

        content_layout = QVBoxLayout()
        content_layout.setSpacing(12)

        stats_container = QFrame()
        stats_container.setStyleSheet(
            "background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px;"
        )
        stats_layout = QHBoxLayout(stats_container)
        stats_layout.setContentsMargins(12, 12, 12, 12)

        self.card_total = self.create_stat_card("Total Equipment")
        self.card_flow = self.create_stat_card("Avg Flowrate (m³/hr)")
        self.card_press = self.create_stat_card("Avg Pressure (bar)")

        stats_layout.addWidget(self.card_total)
        stats_layout.addWidget(self.card_flow)
        stats_layout.addWidget(self.card_press)
        content_layout.addWidget(stats_container)

        action_bar = QFrame()
        action_bar.setStyleSheet(
            "background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px;"
        )
        action_layout = QHBoxLayout(action_bar)
        action_layout.setContentsMargins(12, 10, 12, 10)

        self.add_chart_btn = QPushButton("➕ Add Chart")
        self.add_chart_btn.setStyleSheet(
            "QPushButton { background-color: #10b981; color: white; font-weight: 700; }"
            "QPushButton:hover { background-color: #059669; }"
        )
        self.add_chart_btn.clicked.connect(self.add_chart)

        self.download_btn = QPushButton("⬇ Download Report")
        self.download_btn.clicked.connect(self.save_report)

        action_layout.addWidget(self.add_chart_btn)
        action_layout.addWidget(self.download_btn)
        action_layout.addStretch()
        content_layout.addWidget(action_bar)

        splitter = QSplitter(Qt.Vertical)

        charts_frame = QFrame()
        charts_frame.setStyleSheet(
            "background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px;"
        )
        charts_layout = QVBoxLayout(charts_frame)
        charts_layout.setContentsMargins(8, 8, 8, 8)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(
            "QScrollArea { border: none; background-color: transparent; }"
        )

        self.chart_container = QWidget()
        self.chart_grid = QGridLayout(self.chart_container)
        self.chart_grid.setContentsMargins(8, 8, 8, 8)
        self.chart_grid.setHorizontalSpacing(12)
        self.chart_grid.setVerticalSpacing(12)
        self.scroll_area.setWidget(self.chart_container)
        charts_layout.addWidget(self.scroll_area)

        splitter.addWidget(charts_frame)

        table_frame = QFrame()
        table_frame.setStyleSheet(
            "background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px;"
        )
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(8, 8, 8, 8)

        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_layout.addWidget(self.table)

        splitter.addWidget(table_frame)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 2)

        content_layout.addWidget(splitter)
        main_layout.addLayout(content_layout)

        self.restore_widget_state()
        self.history_widget.refresh()

    def setup_menu_bar(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        upload_action = QAction("Upload CSV", self)
        upload_action.triggered.connect(self.upload_file)
        file_menu.addAction(upload_action)

        download_action = QAction("Download Report", self)
        download_action.triggered.connect(self.save_report)
        file_menu.addAction(download_action)

        file_menu.addSeparator()

        logout_action = QAction("Logout", self)
        logout_action.triggered.connect(self.logout)
        file_menu.addAction(logout_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menubar.addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_stat_card(self, title):
        card = QFrame()
        card.setStyleSheet(
            "background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px;"
        )
        layout = QVBoxLayout(card)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #64748b; font-size: 11px; font-weight: 600;")
        layout.addWidget(lbl_title)

        lbl_value = QLabel("-")
        lbl_value.setStyleSheet("color: #0f172a; font-size: 22px; font-weight: 700;")
        lbl_value.setObjectName("value")
        layout.addWidget(lbl_value)

        return card

    def update_card_value(self, card, value):
        for i in range(card.layout().count()):
            widget = card.layout().itemAt(i).widget()
            if widget.objectName() == "value":
                widget.setText(str(value))

    def add_chart(self):
        chart = ChartWidget()
        chart.setMinimumSize(420, 280)
        chart.closed.connect(self.remove_chart)
        chart.config_changed.connect(self.persist_widget_state)
        self.chart_widgets.append(chart)

        if self.current_rows:
            chart.set_data(self.current_rows, self.current_distribution)

        self.relayout_charts()

        self.persist_widget_state()

    def remove_chart(self, chart):
        if chart in self.chart_widgets:
            self.chart_widgets.remove(chart)
        chart.setParent(None)
        chart.deleteLater()
        self.relayout_charts()
        self.persist_widget_state()

    def persist_widget_state(self):
        try:
            payload = [chart.get_state() for chart in self.chart_widgets]
            self.settings.setValue("chart_widgets", json.dumps(payload))
        except Exception:
            pass

    def restore_widget_state(self):
        stored = self.settings.value("chart_widgets", "")
        restored = []
        if stored:
            try:
                restored = json.loads(stored)
            except Exception:
                restored = []

        if restored:
            for state in restored:
                chart = ChartWidget()
                chart.setMinimumSize(420, 280)
                chart.closed.connect(self.remove_chart)
                chart.config_changed.connect(self.persist_widget_state)
                chart.set_state(state)
                self.chart_widgets.append(chart)
            self.relayout_charts()
        else:
            self.add_chart()

    def relayout_charts(self):
        while self.chart_grid.count():
            item = self.chart_grid.takeAt(0)
            if item and item.widget():
                item.widget().setParent(self.chart_container)

        viewport_width = max(self.scroll_area.viewport().width(), 1)
        card_width = 560
        columns = max(1, viewport_width // card_width)

        for index, chart in enumerate(self.chart_widgets):
            row = index // columns
            col = index % columns
            self.chart_grid.addWidget(chart, row, col)

        self.chart_container.adjustSize()

    def upload_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Open CSV", ".", "CSV Files (*.csv)")
        if fname:
            try:
                self.api_client.upload_file(fname)
                self.history_widget.refresh()
                QMessageBox.information(self, "Success", "Dataset uploaded successfully!")
            except Exception as e:
                error_msg = str(e)
                if hasattr(e, "response") and e.response is not None:
                    try:
                        error_data = e.response.json()
                        error_msg = error_data.get("error", error_msg)
                    except Exception:
                        pass
                QMessageBox.warning(self, "Error", f"Upload failed: {error_msg}")

    def load_batch(self, batch_id):
        self.current_batch_id = batch_id
        try:
            data = self.api_client.get_summary(batch_id)
            summary = data["summary"]

            self.update_card_value(self.card_total, summary["total_count"])
            self.update_card_value(self.card_flow, f"{summary['avg_flow']:.2f}")
            self.update_card_value(self.card_press, f"{summary['avg_press']:.2f}")

            self.current_rows = data.get("data", [])
            self.current_distribution = data.get("type_distribution", {})

            for chart in self.chart_widgets:
                chart.set_data(self.current_rows, self.current_distribution)

            rows = self.current_rows
            self.table.setRowCount(len(rows))
            self.table.setColumnCount(5)
            self.table.setHorizontalHeaderLabels(
                ["Equipment Name", "Type", "Flowrate", "Pressure", "Temperature"]
            )
            for i, row in enumerate(rows):
                self.table.setItem(i, 0, QTableWidgetItem(str(row["equipment_name"])))
                self.table.setItem(i, 1, QTableWidgetItem(str(row["equipment_type"])))
                self.table.setItem(i, 2, QTableWidgetItem(str(row["flowrate"])))
                self.table.setItem(i, 3, QTableWidgetItem(str(row["pressure"])))
                self.table.setItem(i, 4, QTableWidgetItem(str(row["temperature"])))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load data: {str(e)}")

    def save_report(self):
        if not self.current_batch_id:
            QMessageBox.warning(self, "No dataset", "Please select a dataset first.")
            return
        try:
            report_url = self.api_client.get_report_url(self.current_batch_id)
            chart_config = [chart.get_config() for chart in self.chart_widgets]
            response = self.api_client.session.post(
                report_url,
                json={"chart_config": chart_config},
                stream=True,
                timeout=30,
            )
            if response.status_code != 200:
                QMessageBox.warning(self, "Error", "Failed to download report.")
                return

            default_name = f"report_{self.current_batch_id}.pdf"
            save_path, _ = QFileDialog.getSaveFileName(
                self, "Save Report", default_name, "PDF Files (*.pdf)"
            )
            if not save_path:
                return

            with open(save_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            QMessageBox.information(self, "Saved", "Report downloaded successfully.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save report: {str(e)}")

    def on_batch_deleted(self, batch_id):
        if batch_id is None or getattr(self, "current_batch_id", None) == batch_id:
            self.current_batch_id = None
            self.current_rows = []
            self.current_distribution = {}
            self.update_card_value(self.card_total, "-")
            self.update_card_value(self.card_flow, "-")
            self.update_card_value(self.card_press, "-")
            self.table.setRowCount(0)
            for chart in self.chart_widgets:
                chart.set_data([], {})

    def logout(self):
        reply = QMessageBox.question(
            self,
            "Logout",
            "Are you sure you want to logout?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.api_client.logout()
            self.close()

    def show_about(self):
        QMessageBox.about(
            self,
            "About ChemLabWizard",
            "ChemLabWizard - Chemical Data Visualization Platform\n\n"
            "Professional BI Dashboard for equipment analytics.\n"
            "Powered by FOSSEE",
        )

    def closeEvent(self, event):
        self.persist_widget_state()
        super().closeEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.relayout_charts()
