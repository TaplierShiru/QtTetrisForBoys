from main_window.utils import PATH_IMAGE_BACK_NEDDLE
from ..game.shape import Shape
from .draw_block import DrawBlockFrame
from .pressed_frame_controler import PressedFrameControled

from PySide2.QtWidgets import (QWidget, QGridLayout, QVBoxLayout,
                               QHBoxLayout, QPushButton, QLabel
                               )
from PySide2 import QtCore
from PySide2.QtGui import QIcon


class CustomFigureAdder(QWidget):

    ADD_NEW_FIGURE = 3
    MAX_X = 7
    MAX_Y = 7
    MAXIMUM_SIZE = 4

    SHIFT_X = 3
    SHIFT_Y = 3

    def __init__(self, signal_controller):
        super().__init__()

        self.signal_controller = signal_controller

        self.signal_pressed_frames = PressedFrameControled()
        self.signal_pressed_frames.sgn2adder[list].connect(self.take_clicked_frame)

        self.initUI()

    def initUI(self):
        """
        Init widget

        """
        vbox = QVBoxLayout()
        vbox.addSpacing(2)

        # Head
        hbox = QHBoxLayout()
        hbox.addSpacing(3)

        # Create button which returns to the menu
        self._button_back = QPushButton(QIcon(PATH_IMAGE_BACK_NEDDLE), "", self)
        self._button_back.clicked.connect(self.signal_controller.back_to_menu)
        hbox.addWidget(self._button_back, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        # Header of this widget
        self._head_widget = QLabel("Add new figure")
        hbox.addWidget(self._head_widget, 1, QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)

        # Create button to save figure
        self._save_figure_button = QPushButton('save')
        self._save_figure_button.clicked.connect(self.save_figure_shape)
        hbox.addWidget(self._save_figure_button, 2, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)


        vbox.addLayout(hbox, 0)

        grid = QGridLayout()
        self._sheet = []
        self._choose_figure = []
        self._proposed_figures = []
        self._saved_color = 'black'

        for i in range(self.MAX_X):
            row = []
            for j in range(self.MAX_Y):
                single = DrawBlockFrame(self.signal_pressed_frames, j, i)
                if i == 3 and j == 3:
                    single.COLOR_DEFAULT = 'blue'
                    single.default_color()
                row.append(single)
                grid.addWidget(single, i, j)

            self._sheet.append(row)

        vbox.addLayout(grid, 1)

        self.setLayout(vbox)
        self.setWindowTitle("Add new figure")

    def switcher(self):
        """
        Emit signal that menu should be switched to ADD NEW FIGURE widget

        """
        self.signal_controller.sgn2stacked.emit(int(self.ADD_NEW_FIGURE))

    def save_figure_shape(self):
        if len(self._choose_figure) == self.MAXIMUM_SIZE:
            print('save')
            saved_figure = [
                [single[0] - self.SHIFT_X, single[1] - self.SHIFT_Y]
                for single in self._choose_figure
            ]
            Shape.write_figure_data(saved_figure, self._saved_color)

    def __propose_direction(self, to_coordinates):
        propose_move_p = self.__check_figure_propose_move(
            to_coordinates[0], to_coordinates[1]
        )
        print('Propose direction: x: ', to_coordinates[0],' y: ', to_coordinates[1], ' is good: ', propose_move_p)
        if propose_move_p:
            self._proposed_figures[-1].append(to_coordinates)
            self._sheet[to_coordinates[1]][to_coordinates[0]].propose_direction()

    def __check_figure_propose_move(self, to_x, to_y):
        return self.__check_figure_position(to_x, to_y) and \
               not self._sheet[to_y][to_x].is_pressed()

    def __check_figure_position(self, x, y):
        """
        Check whatever x and y is in bounds of the drawing coordinate

        """
        return 0 <= x < self.MAX_X and 0 <= y < self.MAX_Y

    def take_clicked_frame(self, coordinates):

        if len(self._proposed_figures) > 0 and not self._sheet[coordinates[1]][coordinates[0]].is_proposed():
            print('bad direction!')
            return

        # Draw proposed direction (where can move user)
        if len(self._choose_figure) != 0:
            self._proposed_figures.append([])
            # Top direction
            propose_move = [coordinates[0], coordinates[1] - 1]
            self.__propose_direction(propose_move)

            # Left direction
            propose_move = [coordinates[0] - 1, coordinates[1]]
            self.__propose_direction(propose_move)

            # Down direction
            propose_move = [coordinates[0], coordinates[1] + 1]
            self.__propose_direction(propose_move)

            # Right direction
            propose_move = [coordinates[0] + 1, coordinates[1]]
            self.__propose_direction(propose_move)

        if len(self._choose_figure) >= self.MAXIMUM_SIZE:
            coord_del_figure = self._choose_figure.pop(0)
            self._sheet[coord_del_figure[1]][coord_del_figure[0]].default_color()
            self._sheet[coord_del_figure[1]][coord_del_figure[0]].reset_statement()

        # Clear propose direction
        if len(self._proposed_figures) > 1:
            for single_prop in self._proposed_figures[0]:
                self._sheet[single_prop[-1]][single_prop[0]].default_color()
                self._sheet[single_prop[-1]][single_prop[0]].reset_statement()
            self._proposed_figures.pop(0)

        self._choose_figure.append(coordinates[:2])
        self._sheet[coordinates[1]][coordinates[0]].pressed_color()
        print('x: ', coordinates[0], 'y: ', coordinates[1])

