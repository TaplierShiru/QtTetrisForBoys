
from tetris_fb.main_window import MainWindowView

from PySide6.QtWidgets import QApplication
import sys


def main():

    app = QApplication([])
    mainWindow = MainWindowView()
    mainWindow.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
