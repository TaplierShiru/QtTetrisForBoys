
from main_window import MainWindow

from PyQt5.QtWidgets import QApplication
import sys


def main():

    app = QApplication([])
    _ = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
