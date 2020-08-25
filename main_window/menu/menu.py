from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette, QFont
from PyQt5.QtWidgets import (QVBoxLayout, QLabel, QFrame,
                             QPushButton, QWidget,
                             QDesktopWidget, QApplication,
                             )


class MainMenu(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()
    
    def initUI(self):
        """
        Init app

        """
        vbox = QVBoxLayout()

        # Label with name of the game (i.e. Tetris in our case)
        self._label_widget = QLabel("Tetris")
        self._label_widget.setFont(QFont('Times', 20, QFont.Bold))
        self._label_widget.setMaximumHeight(50)
        self._label_widget.setFrameStyle(QFrame.Panel)
        self._label_widget.setStyleSheet("background-color: rgb(200, 160, 160)")
        self._label_widget.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self._label_widget)

        # Create button and widget for game
        self._game_button = QPushButton("Play game")
        pal = self._game_button.palette()
        pal.setColor(QPalette.Button, QColor(Qt.green))
        self._game_button.setAutoFillBackground(True)
        self._game_button.setPalette(pal)
        vbox.addWidget(self._game_button)


        # Create button and widget for settings
        self._settings_button = QPushButton("Settings")
        pal = self._settings_button.palette()
        pal.setColor(QPalette.Button, QColor(Qt.blue))
        self._settings_button.setAutoFillBackground(True)
        self._settings_button.setPalette(pal)
        vbox.addWidget(self._settings_button)


        # Create button and widget about_game
        self._about_game_button = QPushButton("About game")
        pal = self._about_game_button.palette()
        pal.setColor(QPalette.Button, QColor(Qt.yellow))
        self._about_game_button.setAutoFillBackground(True)
        self._about_game_button.setPalette(pal)
        vbox.addWidget(self._about_game_button)

        # Create quit button
        self._exit_button = QPushButton("Exit")
        pal = self._exit_button.palette()
        pal.setColor(QPalette.Button, QColor(Qt.red))
        self._exit_button.setAutoFillBackground(True)
        self._exit_button.setPalette(pal)
        self._exit_button.clicked.connect(QApplication.quit)
        vbox.addWidget(self._exit_button)

        self.setLayout(vbox)
        self.setWindowTitle("Main menu")

    def connect_setting_button(self, connect_to):
        """
        Create event  to show settins, if a button was clicked

        """

        self._settings_button.clicked.connect(connect_to)

    def connect_about_game_button(self, connect_to):
        """
        Create event to show about game, if a button was clicked

        """
        self._about_game_button.clicked.connect(connect_to)

    def connect_game_button(self, connect_to):
        """
        Create event to show game game, if a button was cliked

        """
        self._game_button.clicked.connect(connect_to)

        