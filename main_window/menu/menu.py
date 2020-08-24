from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import (QGridLayout,
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
        grid = QGridLayout()

        # Create button and widget for game
        self._game_button  = QPushButton("Play game")
        pal = self._game_button.palette()
        pal.setColor(QPalette.Button, QColor(Qt.green))
        self._game_button.setAutoFillBackground(True)
        self._game_button.setPalette(pal)
        grid.addWidget(self._game_button, 0, 0)


        # Create button and widget for settings
        self._settings_button = QPushButton("Settings")
        pal = self._settings_button.palette()
        pal.setColor(QPalette.Button, QColor(Qt.blue))
        self._settings_button.setAutoFillBackground(True)
        self._settings_button.setPalette(pal)
        grid.addWidget(self._settings_button, 1, 0)


        # Create button and widget about_game
        self._about_game_button = QPushButton("About game")
        pal = self._about_game_button.palette()
        pal.setColor(QPalette.Button, QColor(Qt.yellow))
        self._about_game_button.setAutoFillBackground(True)
        self._about_game_button.setPalette(pal)
        
        grid.addWidget(self._about_game_button, 2, 0)

        # Create quit button
        self._exit_button = QPushButton("Exit")
        pal = self._exit_button.palette()
        pal.setColor(QPalette.Button, QColor(Qt.red))
        self._exit_button.setAutoFillBackground(True)
        self._exit_button.setPalette(pal)
        self._exit_button.clicked.connect(QApplication.quit)

        grid.addWidget(self._exit_button, 3, 0)

        self.setLayout(grid)
        self.setWindowTitle("Main menu")
    
    def center(self):
        """
        Centers the window on the screen

        """

        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(
            int( (screen.width() - size.width()) / 2),
            int( (screen.height() - size.height()) / 2)
        )

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

        