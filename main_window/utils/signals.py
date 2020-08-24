from main_window.utils import MAIN_MENU_INDEX
from PyQt5.QtCore import pyqtSignal, QObject


class SignalControl(QObject):

    sgn2stacked = pyqtSignal(int)

    def back_to_menu(self):
        """
        Return to start widget
        
        """
        self.sgn2stacked.emit(int(MAIN_MENU_INDEX))

