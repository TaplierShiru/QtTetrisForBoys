from .menu import MainMenuView, TetrisView, SettingsView, AboutGameView, CustomFigureAdderView
from .utils import SignalControl, MAIN_MENU_INDEX

from PySide6.QtWidgets import QGridLayout, QWidget, QStackedWidget, QStatusBar


class MainWindowPresenter(QWidget):

    def __init__(self, statusBar: QStatusBar):
        super().__init__()
        self.statusBar = statusBar
        self.initUI()
    
    def initUI(self):
        """
        Init app

        """
        self._stackedWidget = QStackedWidget(self)

        self._signalController = SignalControl()
        self._signalController.sgn2stacked[int].connect(self._stackedWidget.setCurrentIndex)

        grid = QGridLayout()
        grid.addWidget(self._stackedWidget)

        # Create menu widget
        self._menuWidget = MainMenuView()
        self._stackedWidget.addWidget(self._menuWidget)

        # Create game
        self._gameWidget = TetrisView(self._signalController, self.statusBar)
        self._gameWidget.GAME = self._stackedWidget.addWidget(self._gameWidget)
        self._menuWidget.connect_game_button(self._gameWidget.switcher)

        # Create settings
        self._settingsWidget = SettingsView(self._signalController)
        self._settingsWidget.SETTINGS = self._stackedWidget.addWidget(self._settingsWidget)
        self._menuWidget.connect_setting_button(self._settingsWidget.switcher)

        # Create add new figure widget
        self._addNewFigureWidget = CustomFigureAdderView(self._signalController)
        self._addNewFigureWidget.ABOUT_GAME = self._stackedWidget.addWidget(self._addNewFigureWidget)
        self._menuWidget.connect_add_new_figure_button(self._addNewFigureWidget.switcher)

        # Create about game widget
        self._aboutGameWidget = AboutGameView(self._signalController)
        self._aboutGameWidget.ABOUT_GAME = self._stackedWidget.addWidget(self._aboutGameWidget)
        self._menuWidget.connect_about_game_button(self._aboutGameWidget.switcher)

        self.setLayout(grid)
        self._stackedWidget.setCurrentIndex(MAIN_MENU_INDEX)
        self.setWindowTitle("Main menu")

    def get_settings(self):
        """
        Returns settings widget

        """

        return self._settingsWidget

