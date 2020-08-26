from .control_widget import ControlWidget

from PySide2.QtWidgets import QMainWindow, QDesktopWidget


class MainWindow(QMainWindow):

    WINDOW_SIZE = 'window_size'

    def __init__(self):
        super().__init__()

        self.initUI()
    
    def initUI(self):
        """
        Init app

        """
        self.statusBar = self.statusBar()

        self._control_widget = ControlWidget(self.statusBar)
        self.setCentralWidget(self._control_widget)

        settings_widget = self._control_widget.get_settings()

        self.resize(*settings_widget.get_settings(self.WINDOW_SIZE))
        self.center()
        self.setWindowTitle("Main menu")
        self.show()
    
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

