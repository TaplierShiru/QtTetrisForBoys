from main_window.utils import PATH_IMAGE_BACK_NEDDLE
from .pressed_frame_controler import PressedFrameControled

import random

from PySide2.QtWidgets import (QWidget, QGridLayout, QVBoxLayout,
                               QHBoxLayout, QPushButton, QLabel,
                               QSizePolicy, QFrame)
from PySide2 import QtGui
from PySide2 import QtCore
from PySide2.QtCore import Qt, QTimer
from PySide2.QtGui import QPainter, QPen, QFont, QTransform, QColor, QIcon


class DrawBlockFrame(QFrame):

    def __init__(self, signal_sender_pressed: PressedFrameControled, x: int, y: int):
        super().__init__()

        self._signal_sender_pressed = signal_sender_pressed
        self._x = x
        self._y = y
        self._is_pressed = False
        self._is_proposed = False

        self.initUI()

    def initUI(self):
        """
        Init widget

        """
        self.default_color()

    def default_color(self):
        self.setStyleSheet('QFrame { background-color: blue }')

    def propose_direction(self):
        self._is_proposed = True
        self.setStyleSheet('QFrame { background-color: green }')

    def pressed_color(self):
        self._is_pressed = True
        self.setStyleSheet('QFrame { background-color: black }')

    def reset_statement(self):
        self._is_pressed = False
        self._is_proposed = False

    def enterEvent(self, event: QtCore.QEvent):
        if not self._is_pressed and not self._is_proposed:
            self.setStyleSheet('QFrame { background-color: red }')

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if event.button() == QtCore.Qt.MouseButton.RightButton:
            self._signal_sender_pressed.sgn2adder.emit([self._x, self._y])
