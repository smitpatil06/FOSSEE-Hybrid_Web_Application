from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QToolButton,
    QVBoxLayout,
    QWidget,
    QSizePolicy,
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np


class ChartWidget(QFrame):
    closed = pyqtSignal(object)
    config_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("chartCard")
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(
            "#chartCard { background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; }"
        )

        self._rows = []
        self._distribution = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # Toolbar
        toolbar = QHBoxLayout()
        toolbar.setContentsMargins(0, 0, 0, 0)
        toolbar.setSpacing(8)

        title = QLabel("Chart")
        title.setStyleSheet("color: #1f2937; font-weight: 600; font-size: 11px;")
        toolbar.addWidget(title)

        self.chart_type = QComboBox()
        self.chart_type.addItems(["Bar", "Line", "Scatter", "Pie", "Doughnut", "Area"])
        self.chart_type.currentIndexChanged.connect(self.update_metric_options)

        self.metric = QComboBox()
        self.metric.currentIndexChanged.connect(self._on_config_change)

        self.x_metric = QComboBox()
        self.y_metric = QComboBox()
        self.x_metric.currentIndexChanged.connect(self._on_config_change)
        self.y_metric.currentIndexChanged.connect(self._on_config_change)

        self.theme = QComboBox()
        self.theme.addItems(["Blue", "Red", "Green", "Dark Mode"])
        self.theme.currentIndexChanged.connect(self._on_config_change)

        self.close_btn = QToolButton()
        self.close_btn.setText("✕")
        self.close_btn.setCursor(Qt.PointingHandCursor)
        self.close_btn.setStyleSheet(
            "QToolButton { color: #ef4444; background: transparent; font-weight: bold; }"
            "QToolButton:hover { color: #dc2626; }"
        )
        self.close_btn.clicked.connect(lambda: self.closed.emit(self))

        toolbar.addWidget(self.chart_type)
        toolbar.addWidget(self.metric)
        toolbar.addWidget(self.x_metric)
        toolbar.addWidget(self.y_metric)
        toolbar.addWidget(self.theme)
        toolbar.addStretch()
        toolbar.addWidget(self.close_btn)

        layout.addLayout(toolbar)

        self.figure = Figure(figsize=(5, 3), dpi=100)
        self.figure.patch.set_facecolor("#ffffff")
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.canvas)

        self._init_metric_sets()
        self.update_metric_options()

    def sizeHint(self):
        return QSize(560, 340)

    def minimumSizeHint(self):
        return QSize(480, 280)

    def set_data(self, rows, distribution=None):
        self._rows = rows or []
        if distribution is None or distribution == {}:
            dist = {}
            for row in self._rows:
                key = str(row.get("equipment_type", "Unknown"))
                dist[key] = dist.get(key, 0) + 1
            self._distribution = dist
        else:
            self._distribution = distribution
        self.refresh()

    def _get_theme(self):
        theme = self.theme.currentText()
        if theme == "Red":
            return "#ef4444", "#fecaca", "#111827", "#ffffff"
        if theme == "Green":
            return "#10b981", "#bbf7d0", "#111827", "#ffffff"
        if theme == "Dark Mode":
            return "#1f2937", "#9ca3af", "#111827", "#ffffff"
        return "#3b82f6", "#93c5fd", "#111827", "#ffffff"

    def _init_metric_sets(self):
        self._categorical_metrics = [("Type Distribution", "type_distribution")]
        self._continuous_metrics = [
            ("Flowrate", "flowrate"),
            ("Pressure", "pressure"),
            ("Temperature", "temperature"),
        ]
        self._metric_label_map = {
            "type_distribution": "Type Distribution",
            "flowrate": "Flowrate",
            "pressure": "Pressure",
            "temperature": "Temperature",
        }

    def _set_combo_items(self, combo, items):
        combo.blockSignals(True)
        combo.clear()
        for label, key in items:
            combo.addItem(label, key)
        combo.blockSignals(False)

    def update_metric_options(self):
        chart_type = self.chart_type.currentText().lower()
        if chart_type in ["pie", "doughnut"]:
            items = self._categorical_metrics
        elif chart_type in ["line", "area"]:
            items = self._continuous_metrics
        elif chart_type == "scatter":
            items = []
        else:
            items = self._categorical_metrics + self._continuous_metrics

        if chart_type == "scatter":
            self.metric.setVisible(False)
            self.x_metric.setVisible(True)
            self.y_metric.setVisible(True)
            self._set_combo_items(self.x_metric, self._continuous_metrics)
            self._set_combo_items(self.y_metric, self._continuous_metrics)
        else:
            self.metric.setVisible(True)
            self.x_metric.setVisible(False)
            self.y_metric.setVisible(False)
            self._set_combo_items(self.metric, items)

        self.refresh()
        self.config_changed.emit()

    def _on_config_change(self):
        self.refresh()
        self.config_changed.emit()

    def _series(self, key):
        values = []
        labels = []
        for row in self._rows:
            try:
                values.append(float(row.get(key, 0)))
                labels.append(str(row.get("equipment_name", "")))
            except Exception:
                continue
        return labels, values

    def refresh(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        primary, accent, text_color, bg_color = self._get_theme()
        self.figure.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)

        chart_type = self.chart_type.currentText()
        metric_key = self.metric.currentData()

        if not self._rows and not self._distribution:
            ax.text(
                0.5,
                0.5,
                "No data loaded",
                ha="center",
                va="center",
                fontsize=12,
                color=text_color,
            )
            ax.axis("off")
        elif metric_key == "type_distribution":
            labels = list(self._distribution.keys())
            values = list(self._distribution.values())
            if chart_type in {"Pie", "Doughnut"}:
                wedges, *_ = ax.pie(values, labels=labels, autopct="%1.0f%%")
                for w in wedges:
                    w.set_edgecolor("#0f172a")
                if chart_type == "Doughnut":
                    centre_circle = plt.Circle((0, 0), 0.65, fc=bg_color)
                    ax.add_artist(centre_circle)
            else:
                ax.bar(labels, values, color=primary, alpha=0.85)
                ax.set_ylabel("Count", color=text_color)
                ax.tick_params(axis="x", rotation=20)
        elif chart_type == "Scatter":
            x_key = self.x_metric.currentData()
            y_key = self.y_metric.currentData()
            x_labels, x_vals = self._series(x_key)
            y_labels, y_vals = self._series(y_key)
            length = min(len(x_vals), len(y_vals))
            x_vals = x_vals[:length]
            y_vals = y_vals[:length]
            ax.scatter(x_vals, y_vals, color=primary, alpha=0.8)
            ax.set_xlabel(x_key, color=text_color)
            ax.set_ylabel(y_key, color=text_color)
        else:
            labels, values = self._series(metric_key)
            labels = labels[:20]
            values = values[:20]
            x_idx = np.arange(len(values))
            if chart_type == "Line":
                ax.plot(x_idx, values, color=primary, marker="o")
            elif chart_type == "Scatter":
                ax.scatter(x_idx, values, color=primary, alpha=0.8)
            elif chart_type == "Pie" or chart_type == "Doughnut":
                display_labels = labels[:8]
                display_values = values[:8]
                wedges, *_ = ax.pie(display_values, labels=display_labels, autopct="%1.0f%%")
                for w in wedges:
                    w.set_edgecolor("#0f172a")
                if chart_type == "Doughnut":
                    centre_circle = plt.Circle((0, 0), 0.65, fc=bg_color)
                    ax.add_artist(centre_circle)
            elif chart_type == "Area":
                ax.plot(x_idx, values, color=primary)
                ax.fill_between(x_idx, values, color=accent, alpha=0.4)
            else:
                ax.bar(x_idx, values, color=primary, alpha=0.85)

            ax.set_xticks(x_idx)
            ax.set_xticklabels(labels, rotation=20, fontsize=8, color=text_color)
            ax.set_ylabel(metric_key, color=text_color)

        ax.tick_params(axis="y", colors=text_color)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color(text_color)
        ax.spines["bottom"].set_color(text_color)
        ax.title.set_color(text_color)
        title_metric = self.metric.currentText() if chart_type != "Scatter" else f"{self.x_metric.currentText()} vs {self.y_metric.currentText()}"
        ax.set_title(f"{title_metric} ({chart_type})", color=text_color, fontsize=10)
        self.figure.tight_layout()
        self.canvas.draw_idle()

    def get_config(self):
        chart_type = self.chart_type.currentText().lower()
        theme_map = {
            "Blue": "#3b82f6",
            "Red": "#ef4444",
            "Green": "#10b981",
            "Dark Mode": "#1f2937",
        }

        if chart_type == "scatter":
            metric_key = f"{self.x_metric.currentData()}_vs_{self.y_metric.currentData()}"
            title = f"{self.x_metric.currentText()} vs {self.y_metric.currentText()}"
        else:
            metric_key = self.metric.currentData()
            title = self.metric.currentText()

        if chart_type in ["pie", "doughnut"]:
            color = "multi"
        else:
            color = theme_map.get(self.theme.currentText(), "#3b82f6")

        return {
            "type": chart_type,
            "metric": metric_key or "type_distribution",
            "title": f"{title} ({chart_type.title()})",
            "color": color,
        }

    def get_state(self):
        chart_type = self.chart_type.currentText()
        metric_key = self.metric.currentData()
        return {
            "chart_type": chart_type,
            "metric": metric_key,
            "theme": self.theme.currentText(),
            "x_metric": self.x_metric.currentData(),
            "y_metric": self.y_metric.currentData(),
        }

    def set_state(self, state):
        chart_type = state.get("chart_type", "Bar")
        self.chart_type.setCurrentText(chart_type)
        if chart_type.lower() == "scatter":
            x_metric = state.get("x_metric", "flowrate")
            y_metric = state.get("y_metric", "pressure")
            self.x_metric.setCurrentIndex(self.x_metric.findData(x_metric))
            self.y_metric.setCurrentIndex(self.y_metric.findData(y_metric))
        else:
            metric_key = state.get("metric", "type_distribution")
            self.metric.setCurrentIndex(self.metric.findData(metric_key))
        theme = state.get("theme", "Blue")
        self.theme.setCurrentText(theme)
        self.refresh()
