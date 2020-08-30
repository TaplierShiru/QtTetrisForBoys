
from main_window.utils import PATH_IMAGE_BACK_NEDDLE, PATH_IMAGE_RELOAD
from .board import Board

from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLCDNumber, QLabel
from PySide2 import QtCore


class Tetris(QWidget):

    GAME = 1

    def __init__(self, signal_controller, status_bar):
        super().__init__()

        self.signal_controller = signal_controller
        self.statusBar = status_bar
        self.initUI()
    
    def initUI(self):
        """
        Init app

        """
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        # Create button "back to the menu"
        self._button_back = QPushButton(QIcon(PATH_IMAGE_BACK_NEDDLE), "", self)
        self._button_back.clicked.connect(self.signal_controller.back_to_menu)
        self._button_back.setFixedSize(60, 30)
        vbox.addWidget(self._button_back, 0, QtCore.Qt.AlignTop)

        self.tboard = Board(self)

        # Create button which restart game
        self._restart_game = QPushButton(QIcon(PATH_IMAGE_RELOAD), "", self)
        self._restart_game.clicked.connect(self.tboard.start)
        self._restart_game.setFixedSize(60, 30)
        vbox.addWidget(self._restart_game, 1, QtCore.Qt.AlignTop)

        # Create label "Score"
        self._label_score = QLabel("Game Score", self)
        vbox.addWidget(self._label_score, 2, QtCore.Qt.AlignBottom)

        # Create score counter
        self._score = QLCDNumber(self)
        self._score.setFixedSize(70, 50)
        vbox.addWidget(self._score, 3, QtCore.Qt.AlignTop)

        hbox.addLayout(vbox, 0)
        hbox.addWidget(self.tboard, 1)

        self.setLayout(hbox)
        self.setWindowTitle("Tetris")

        self.tboard.msg2StatusBar[str].connect(self._score.display)

    def switcher(self):
        self.tboard.start()
        self.signal_controller.sgn2stacked.emit(int(self.GAME))

