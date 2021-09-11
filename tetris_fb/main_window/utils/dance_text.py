import random

from PySide6.QtWidgets import QFrame
from PySide6 import QtGui
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QPen, QFont, QTransform, QColor


class DanceText(QFrame):

    def __init__(self, text, parent):
        super().__init__(parent)

        self._text = text
        # Variables for rotation
        self._rotate = 0
        self._add_rotation = 1

        # Variables for scale, for [x, y] axis
        self._scale = [100, 100]
        self._add_scale = [1, 1]

        self.initUI()

    def initUI(self):
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.update)
        self._timer.start(50)

    def get_text(self):
        return self._text

    def set_text(self):
        return self._text

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        painter = QPainter(self)
        #painter.setPen(QPen(Qt.blue, 1, Qt.DashLine))

        # Create transformation for text and other things that will be drawn
        transform = QTransform()
        # Rotation
        shift_x = self.width() // 2     #self.geometry().width() // 2
        shift_y = self.height() // 2    #self.geometry().height() // 2
        transform.translate(shift_x, shift_y)
        transform.rotate(self._rotate)
        transform.translate(-shift_x, -shift_y)

        # Scale, NOTICE! Scale change position of the text, i. e. size of frame (?)
        scale_x = self._scale[0] / 100   #random.randint(80, 200) / 100
        scale_y = self._scale[1] / 100   #random.randint(90, 120) / 100
        transform.scale(scale_x, scale_y)

        # Apply transformation
        painter.setTransform(transform)

        # Draw text
        painter.setFont(QFont('Times', 20, QFont.Bold))
        painter.setPen(QPen(QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 1))
        # Because of the scale size of the frame is changed, recalculate size according to scale
        width_tr = int(self.width() * (1 / scale_x))
        height_tr = int(self.height() * (1 / scale_y))
        painter.drawText(0, 0, width_tr, height_tr, Qt.AlignCenter | Qt.AlignTop, self._text)

        # Update transformation variables
        self._rotate += self._add_rotation
        self._scale[0] += self._add_scale[0]
        self._scale[1] += self._add_scale[1]
        # Check bounds and keep variable in the loop
        if self._rotate > 30 or self._rotate < -30:
            self._add_rotation *= (-1)

        if self._scale[0] > 200 or self._scale[0] < 70:
            self._add_scale[0] *= (-1)

        if self._scale[1] > 130 or self._scale[1] < 80:
            self._add_scale[1] *= (-1)

