import random

from PySide2.QtWidgets import QFrame
from PySide2 import QtGui
from PySide2.QtCore import Qt, QTimer
from PySide2.QtGui import QPainter, QPen, QFont, QTransform, QColor


class DanceText(QFrame):
    """
    Draw QFrame with 'dance' text.
    'Dance' mean that this text is similar to main menu from Hotline Miami.

    """

    def __init__(
            self,
            text,
            parent,
            start_rotation=0,
            rotation_bounds=[-30, 30],
            rotation_speed=1.5,
            start_scale=[100, 100],
            scale_bounds=[[200, 70], [130, 80]],
            scale_speed=[1, 1],
    ):
        """
        Init DanceText widget

        Parameters
        ----------
        text : str
            Text that will be shown on this widget
        parent : PySide2.QtWidgets.QWidget
            Parent widget
        start_rotation : float
            Start angle of the text, measured in degrees
        rotation_bounds : list
            Bounds of value that can accept rotation of the text, measured in degrees.
            By default equal to [-30, 30] (order is don't matter)
        rotation_speed : float
            Speed of the changes in the rotation.
            By default equal to 1, i.e. for one clock rotation of the text changes to 1 degree
        start_scale : list
            Start scale coefficient of the text for each axis (x and y), measured in percent,
            For example 100 - mean that size is 100%, 65 - 65% (of maximum size) and etc...
            By default equal to [100, 100], i.e. for x and y axis scale is full size.
        scale_bounds : list
            Bounds of value that can accept scale of the text for each axis (x and y), measured in percent.
            By default equal to [[200, 70], [130, 80]] (order is don't matter),
            I.e. for x axis bounds - [200, 70], for y axis bounds - [130, 80]
        scale_speed : list
            Speed of the changes in the scale for each axis (x and y)
            By default equal to [1, 1], i.e. for one clock size of the text for x and y axis changes to 1 percent

        """
        super().__init__(parent)

        self._text = str(text)
        # Variables for rotation
        self._rotate = start_rotation
        self._rotation_bounds = rotation_bounds
        self._add_rotation = rotation_speed

        # Variables for scale, for [x, y] axis
        self._scale = start_scale
        self._scale_bounds = scale_bounds
        self._add_scale = scale_speed

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
        shift_x = self.width() // 2
        shift_y = self.height() // 2
        transform.translate(shift_x, shift_y)
        transform.rotate(self._rotate)
        transform.translate(-shift_x, -shift_y)

        # Scale, NOTICE! Scale change position of the text, i. e. size of frame (?)
        scale_x = self._scale[0] / 100
        scale_y = self._scale[1] / 100
        transform.scale(scale_x, scale_y)

        # Apply transformation
        painter.setTransform(transform)

        # Draw text
        painter.setFont(QFont('Times', 20, QFont.Bold))
        painter.setPen(
            QPen(
                QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                1
            )
        )
        # Because of the scale size of the frame is changed, recalculate size according to scale
        width_tr = int(self.width() * (1 / scale_x))
        height_tr = int(self.height() * (1 / scale_y))
        painter.drawText(0, 0, width_tr, height_tr, Qt.AlignCenter | Qt.AlignTop, self._text)

        # Update transformation variables
        self._rotate += self._add_rotation
        self._scale[0] += self._add_scale[0]
        self._scale[1] += self._add_scale[1]
        # Check bounds and keep variable in the loop
        if self._rotate >= max(self._rotation_bounds) or self._rotate <= min(self._rotation_bounds):
            self._add_rotation *= (-1)

        if self._scale[0] >= max(self._scale_bounds[0]) or self._scale[0] <= min(self._scale_bounds[0]):
            self._add_scale[0] *= (-1)

        if self._scale[1] >= max(self._scale_bounds[1]) or self._scale[1] <= min(self._scale_bounds[1]):
            self._add_scale[1] *= (-1)

