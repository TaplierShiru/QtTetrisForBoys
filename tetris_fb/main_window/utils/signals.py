from tetris_fb.main_window.utils import MAIN_MENU_INDEX
from PySide6.QtCore import Signal, QObject


class SignalControl(QObject):

    sgn2stacked = Signal(int)

    def back2menu(self):
        """
        Return to start widget
        
        """
        self.sgn2stacked.emit(int(MAIN_MENU_INDEX))

