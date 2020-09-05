from .pressed_frame_controler import PressedFrameControled

from PySide2.QtWidgets import QFrame
from PySide2 import QtGui
from PySide2 import QtCore


class DrawBlockFrame(QFrame):
    COLOR_DEFAULT = '#F8F8FF'
    COLOR_PRESSED = '#708090'
    COLOR_PROPOSE = '#90EE90'
    COLOR_LOOK_AT = '#87CEFA'

    def __init__(self, signal_sender_pressed: PressedFrameControled, x: int, y: int):
        """
        Create DrawBlockFrame for drawing new figures

        Parameters
        ----------
        signal_sender_pressed : PressedFrameControled
            Controller for emit signals to CustomFigureAdder widget
        x : int
            Coordinate on X axis for this block
        y : int
            Coordinate on Y axis for this block

        """
        super().__init__()

        self._signal_sender_pressed = signal_sender_pressed
        self._x = x
        self._y = y
        # Current statement for this frame
        self._is_pressed = False
        self._is_proposed = False

        self.initUI()

    def initUI(self):
        """
        Init widget

        """
        self.default_color()

    def default_color(self):
        """
        Reset color to default color (blue)

        """
        self.setStyleSheet('QFrame { background-color: %s;\n' % self.COLOR_DEFAULT + \
                           'border: 1px solid;\n' + \
                           'padding: 10px; }')

    def propose_direction(self):
        """
        Set propose color and set block into propose statement

        """
        self._is_proposed = True
        self.setStyleSheet('QFrame { background-color: %s }' % self.COLOR_PROPOSE)

    def pressed_color(self):
        """
        Set pressed color and set block into pressed statement

        """
        self._is_pressed = True
        self.setStyleSheet('QFrame { background-color: %s }' % self.COLOR_PRESSED)

    def is_pressed(self):
        """
        Return bool statement pressed block or not

        """
        return self._is_pressed

    def is_proposed(self):
        """
        Return bool statement proposed block or not

        """
        return self._is_proposed

    def reset_statement(self):
        """
        Reset statement for this block

        """
        self._is_pressed = False
        self._is_proposed = False

    def enterEvent(self, event: QtCore.QEvent):
        """
        Event which control enter of the mouse into this widget

        """
        if not self._is_pressed and not self._is_proposed:
            self.setStyleSheet('QFrame { background-color: %s }' % self.COLOR_LOOK_AT)

    def leaveEvent(self, event: QtCore.QEvent):
        """
        Event which control leave of the mouse from this widget

        """
        if not self._is_pressed and not self._is_proposed:
            self.default_color()

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        """
        Event for pressing certain mouse buttons on this widget

        """
        if event.button() == QtCore.Qt.MouseButton.RightButton:
            self._signal_sender_pressed.sgn2adder.emit([self._x, self._y])
