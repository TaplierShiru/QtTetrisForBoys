
from tetris_fb.main_window import MainWindow

from PySide6.QtWidgets import QApplication
import sys


def main():

    app = QApplication([])
    _ = MainWindow()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
