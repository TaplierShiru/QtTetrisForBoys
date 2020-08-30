from .menu import MainMenu, Tetris, Settings, AboutGame
from .utils import SignalControl, MAIN_MENU_INDEX

from PySide2.QtWidgets import QGridLayout, QWidget, QStackedWidget


class ControlWidget(QWidget):

    def __init__(self, status_bar):
        super().__init__()
        self.statusBar = status_bar
        self.initUI()
    
    def initUI(self):
        """
        Init app

        """
        self._stacked_widget = QStackedWidget(self)

        self._signal_controller = SignalControl()
        self._signal_controller.sgn2stacked[int].connect(self._stacked_widget.setCurrentIndex)

        grid = QGridLayout()
        grid.addWidget(self._stacked_widget)

        # Create menu widget
        self._menu_widget = MainMenu()
        self._stacked_widget.addWidget(self._menu_widget)

        # Create game
        self._game_widget = Tetris(self._signal_controller, self.statusBar)
        self._game_widget.GAME = self._stacked_widget.addWidget(self._game_widget)
        self._menu_widget.connect_game_button(self._game_widget.switcher)

        # Create settings
        self._settings_widget = Settings(self._signal_controller)
        self._settings_widget.SETTINGS = self._stacked_widget.addWidget(self._settings_widget)
        self._menu_widget.connect_setting_button(self._settings_widget.switcher)

        # Create about game widget
        self._about_game_widget = AboutGame(self._signal_controller)
        self._about_game_widget.ABOUT_GAME = self._stacked_widget.addWidget(self._about_game_widget)
        self._menu_widget.connect_about_game_button(self._about_game_widget.switcher)

        self.setLayout(grid)
        self._stacked_widget.setCurrentIndex(MAIN_MENU_INDEX)
        self.setWindowTitle("Main menu")

    def get_settings(self):
        """
        Returns settings widget

        """

        return self._settings_widget

