from tetris_fb.main_window.utils import PATH_IMAGE_BACK_NEDDLE
from .utils import  ABOUT_GAME_STR

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
from PySide6 import QtCore
from PySide6.QtGui import QFont, QIcon


class AboutGameView(QWidget):

    ABOUT_GAME = 4

    def __init__(self, signalController):
        super().__init__()
        self.signalController = signalController

        self.initUI()
    
    def initUI(self):
        """
        Init widget

        """
        vbox = QVBoxLayout()
        vbox.addSpacing(2)
        
        # Head
        hbox = QHBoxLayout()
        hbox.addSpacing(2)

        # Create button which returns to the menu
        self._buttonBack = QPushButton(QIcon(PATH_IMAGE_BACK_NEDDLE), "", self)
        self._buttonBack.clicked.connect(self.signalController.back2menu)
        hbox.addWidget(self._buttonBack, 0, QtCore.Qt.AlignLeft)
        # Header of this widget
        self._headWidget = QLabel("About game")
        hbox.addWidget(self._headWidget, 1, QtCore.Qt.AlignCenter)

        vbox.addLayout(hbox, 0)
        
        # Create text about game
        text = ABOUT_GAME_STR
        self.textAboutGame = QLabel(text)
        self.textAboutGame.setWordWrap(True)
        self.setFont(QFont("Times", 12, QFont.Bold))
        vbox.addWidget(self.textAboutGame, 1, QtCore.Qt.AlignCenter)

        self.setLayout(vbox)
        self.setWindowTitle("About game")
    
    def switcher(self):
        """
        Emit signal that menu should be switched to ABOUT GAME widget

        """
        self.signalController.sgn2stacked.emit(int(self.ABOUT_GAME))

