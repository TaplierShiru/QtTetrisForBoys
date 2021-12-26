import random

from PySide6.QtWidgets import QFrame
from PySide6 import QtGui
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QPen, QFont, QTransform, QColor


class DanceText(QFrame):
    """
    Draw QFrame with 'dance' text.
    'Dance' mean that this text is similar to main menu from Hotline Miami.

    """

    def __init__(
            self,
            text,
            parent,
            startRotation=0,
            rotationBounds=[-30, 30],
            rotation_speed=1.5,
            startScale=[100, 100],
            scaleBounds=[[200, 70], [130, 80]],
            scaleSpeed=[1, 1],
    ):
        """
        Init DanceText widget

        Parameters
        ----------
        text : str
            Text that will be shown on this widget
        parent : PySide2.QtWidgets.QWidget
            Parent widget
        startRotation : float
            Start angle of the text, measured in degrees
        rotationBounds : list
            Bounds of value that can accept rotation of the text, measured in degrees.
            By default equal to [-30, 30] (order is don't matter)
        rotation_speed : float
            Speed of the changes in the rotation.
            By default equal to 1, i.e. for one clock rotation of the text changes to 1 degree
        startScale : list
            Start scale coefficient of the text for each axis (x and y), measured in percent,
            For example 100 - mean that size is 100%, 65 - 65% (of maximum size) and etc...
            By default equal to [100, 100], i.e. for x and y axis scale is full size.
        scaleBounds : list
            Bounds of value that can accept scale of the text for each axis (x and y), measured in percent.
            By default equal to [[200, 70], [130, 80]] (order is don't matter),
            I.e. for x axis bounds - [200, 70], for y axis bounds - [130, 80]
        scaleSpeed : list
            Speed of the changes in the scale for each axis (x and y)
            By default equal to [1, 1], i.e. for one clock size of the text for x and y axis changes to 1 percent

        """
        super().__init__(parent)

        self._text = str(text)
        # Variables for rotation
        self._rotate = startRotation
        self._rotationBounds = rotationBounds
        self._addRotation = rotation_speed

        # Variables for scale, for [x, y] axis
        self._scale = startScale
        self._scaleBounds = scaleBounds
        self._addScale = scaleSpeed

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
        shiftX = self.width() // 2
        shiftY = self.height() // 2
        transform.translate(shiftX, shiftY)
        transform.rotate(self._rotate)
        transform.translate(-shiftX, -shiftY)

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
        self._rotate += self._addRotation
        self._scale[0] += self._addScale[0]
        self._scale[1] += self._addScale[1]
        # Check bounds and keep variable in the loop
        if self._rotate >= max(self._rotationBounds) or self._rotate <= min(self._rotationBounds):
            self._addRotation *= (-1)

        if self._scale[0] >= max(self._scaleBounds[0]) or self._scale[0] <= min(self._scaleBounds[0]):
            self._addScale[0] *= (-1)

        if self._scale[1] >= max(self._scaleBounds[1]) or self._scale[1] <= min(self._scaleBounds[1]):
            self._addScale[1] *= (-1)

