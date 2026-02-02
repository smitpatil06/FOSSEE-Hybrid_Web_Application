from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class ChartsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.figure = Figure(figsize=(5, 3), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    def update_chart(self, distribution):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        if distribution:
            ax.bar(distribution.keys(), distribution.values(), color=['#3B82F6','#10B981','#F59E0B','#EF4444','#8B5CF6','#EC4899'])
        ax.set_title('Equipment Type Distribution')
        ax.tick_params(axis='x', rotation=20)
        self.figure.tight_layout()
        self.canvas.draw()
