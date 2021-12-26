from .main_window_presenter import MainWindowPresenter

from PySide6.QtWidgets import QMainWindow


class MainWindowView(QMainWindow):

    WINDOW_SIZE = 'window_size'

    def __init__(self):
        super().__init__()

        self.initUI()
    
    def initUI(self):
        """
        Init app

        """
        self.statusBar = self.statusBar()

        self._controlWidget = MainWindowPresenter(self.statusBar)
        self.setCentralWidget(self._controlWidget)

        settingsWidget = self._controlWidget.get_settings()

        self.resize(*settingsWidget.get_settings(self.WINDOW_SIZE))
        self.center()
        self.setWindowTitle("Main menu")
    
    def center(self):
        """
        Centers the window on the screen

        """
        screen = self.screen().geometry()
        size = self.geometry()
        self.move(
            int( (screen.width() - size.width()) / 2),
            int( (screen.height() - size.height()) / 2)
        )

