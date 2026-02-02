from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class ChartsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        self.title_label = QLabel("Equipment Type Distribution")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #1e293b; padding: 10px;")
        layout.addWidget(self.title_label)
        
        # Chart
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.figure.patch.set_facecolor('#f5f7fa')
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        self.setLayout(layout)
        self.setStyleSheet("background-color: white; border-radius: 8px; border: 1px solid #e2e8f0;")
    
    def update_chart(self, type_distribution):
        """Update chart with new data"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        if type_distribution:
            labels = list(type_distribution.keys())
            values = list(type_distribution.values())
            
            # Bar chart with FOSSEE-like colors
            colors = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899']
            ax.bar(labels, values, color=colors[:len(labels)], alpha=0.7)
            
            ax.set_title("Equipment Type Distribution", fontsize=11, color='#333', pad=10)
            ax.set_xlabel("Equipment Type", fontsize=9, color='#666')
            ax.set_ylabel("Count", fontsize=9, color='#666')
            ax.tick_params(axis='x', rotation=25, labelsize=8)
            ax.tick_params(axis='y', labelsize=8)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.grid(axis='y', alpha=0.2, linestyle='--')
            
        self.figure.tight_layout()
        self.canvas.draw()
    
    def clear_chart(self):
        """Clear the chart"""
        self.figure.clear()
        self.canvas.draw()
