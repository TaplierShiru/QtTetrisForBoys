
from tetris_fb.main_window.utils import PATH_IMAGE_BACK_NEDDLE, PATH_IMAGE_RELOAD
from .board import Board

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLCDNumber, QLabel
from PySide6 import QtCore


class TetrisView(QWidget):

    GAME = 1

    def __init__(self, signalController, status_bar):
        super().__init__()

        self.signalController = signalController
        self.statusBar = status_bar
        self.initUI()
    
    def initUI(self):
        """
        Init app

        """
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        # Create button "back to the menu"
        self._buttonBack = QPushButton(QIcon(PATH_IMAGE_BACK_NEDDLE), "", self)
        self._buttonBack.clicked.connect(self.signalController.back2menu)
        self._buttonBack.setFixedSize(60, 30)
        vbox.addWidget(self._buttonBack, 0, QtCore.Qt.AlignTop)

        self.tboard = Board(self)

        # Create button which restart game
        self._restartGame = QPushButton(QIcon(PATH_IMAGE_RELOAD), "", self)
        self._restartGame.clicked.connect(self.tboard.start)
        self._restartGame.setFixedSize(60, 30)
        vbox.addWidget(self._restartGame, 1, QtCore.Qt.AlignTop)

        # Create label "Score"
        self._labelScore = QLabel("Game Score", self)
        vbox.addWidget(self._labelScore, 2, QtCore.Qt.AlignBottom)

        # Create score counter
        self._score = QLCDNumber(self)
        self._score.setFixedSize(70, 50)
        vbox.addWidget(self._score, 3, QtCore.Qt.AlignTop)

        hbox.addLayout(vbox, 0)
        hbox.addWidget(self.tboard, 1)

        self.setLayout(hbox)
        self.setWindowTitle("TetrisView")

        self.tboard.msg2StatusBar[str].connect(self._score.display)

    def switcher(self):
        self.tboard.start()
        self.signalController.sgn2stacked.emit(int(self.GAME))

