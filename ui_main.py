# -*- coding: utf-8 -*-
"""IQplayer Qt6 interface"""

from PySide6.QtCore import QRectF, QTimer, Qt
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtWidgets import QGridLayout, QMainWindow, QVBoxLayout, QWidget


class CircularSpinner(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.angle = 0
        self.setFixedSize(50, 50)  # Tamaño del spinner

        # Timer para animar la rotación (30 FPS aproximados)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate)
        self.timer.start(16)

    def rotate(self):
        self.angle = (self.angle + 8) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = QRectF(5, 5, self.width() - 10, self.height() - 10)

        # Estilo de la línea (ancho 4px, color azul Qt)
        pen = QPen(QColor(41, 128, 185), 4)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)

        # QPainter usa ángulos en 1/16 de grado
        start_angle = -self.angle * 16
        span_angle = 280 * 16  # Longitud del arco (280 grados)

        painter.drawArc(rect, start_angle, span_angle)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(central_widget)
        self.spinner = CircularSpinner()
        layout.addWidget(self.spinner)
        self.results_layout = QGridLayout()
        layout.addLayout(self.results_layout)
