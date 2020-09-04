from main_window.utils import PATH_IMAGE_BACK_NEDDLE

from PySide2.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
from PySide2 import QtCore
from PySide2.QtGui import QFont, QIcon


class AboutGame(QWidget):

    ABOUT_GAME = 4

    def __init__(self, signal_controller):
        super().__init__()
        self.signal_controller = signal_controller

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
        self._button_back = QPushButton(QIcon(PATH_IMAGE_BACK_NEDDLE), "", self)
        self._button_back.clicked.connect(self.signal_controller.back_to_menu)
        hbox.addWidget(self._button_back, 0, QtCore.Qt.AlignLeft)
        # Header of this widget
        self._head_widget = QLabel("About game")
        hbox.addWidget(self._head_widget, 1, QtCore.Qt.AlignCenter)

        vbox.addLayout(hbox, 0)
        
        # Create text about game
        text = "This game is made to improve my competence in Qt " + \
               "and just for fun. Thanks for playing this game or " + \
               "just visited this code for study in Qt"
        self.text_about_game = QLabel(text)
        self.text_about_game.setWordWrap(True)
        self.setFont(QFont("Times", 12, QFont.Bold))
        vbox.addWidget(self.text_about_game, 1, QtCore.Qt.AlignCenter)

        self.setLayout(vbox)
        self.setWindowTitle("About game")
    
    def switcher(self):
        """
        Emit signal that menu should be switched to ABOUT GAME widget

        """
        self.signal_controller.sgn2stacked.emit(int(self.ABOUT_GAME))

