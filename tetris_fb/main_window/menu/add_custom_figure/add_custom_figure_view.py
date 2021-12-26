from tetris_fb.main_window.utils import PATH_IMAGE_BACK_NEDDLE
from ..game.shape import Shape
from .draw_block import DrawBlockQFrame
from .pressed_frame_controller import PressedFrameController

from PySide6.QtWidgets import (QWidget, QGridLayout, QVBoxLayout,
                               QHBoxLayout, QPushButton, QLabel, QColorDialog)
from PySide6 import QtCore
from PySide6.QtGui import QIcon


class CustomFigureAdderView(QWidget):

    ADD_NEW_FIGURE = 3
    MAX_X = 7
    MAX_Y = 7
    MAXIMUM_SIZE = 5

    SHIFT_X = 3
    SHIFT_Y = 3

    def __init__(self, signalController):
        super().__init__()

        self.signalController = signalController

        self.signalPressedFrames = PressedFrameController()
        self.signalPressedFrames.sgn2adder[list].connect(self.take_clicked_frame)

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
        self._buttonBack = QPushButton(QIcon(PATH_IMAGE_BACK_NEDDLE), "", self)
        self._buttonBack.clicked.connect(self.signalController.back2menu)
        hbox.addWidget(self._buttonBack, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        # Header of this widget
        self._headWidget = QLabel("Add new figure")
        hbox.addWidget(self._headWidget, 1, QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)

        # Create button to choose color of new figure
        self._pickColorButton = QPushButton('Pick color')
        self._pickColorButton.clicked.connect(self.update_color_name)
        hbox.addWidget(self._pickColorButton, 2, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)

        # Create button to save figure
        self._saveFigureButton = QPushButton('Save')
        self._saveFigureButton.clicked.connect(self.save_figure_shape)
        hbox.addWidget(self._saveFigureButton, 2, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)

        vbox.addLayout(hbox, 0)

        grid = QGridLayout()
        self._sheet = []
        self._choosenFigureList = []
        self._proposedFiguresList = []
        self._savedColor = 'black'

        for i in range(self.MAX_X):
            row = []
            for j in range(self.MAX_Y):
                single = DrawBlockQFrame(self.signalPressedFrames, j, i)
                if i == 3 and j == 3:
                    # Button in the center - must be with blur color
                    # Save figure - possible only if blue button also clicked
                    # This magic stuff are made in order to simplify saving figure
                    single.COLOR_DEFAULT = 'blue'
                    single.default_color()
                    self.centerSheet = single
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
        self.signalController.sgn2stacked.emit(int(self.ADD_NEW_FIGURE))

    def update_color_name(self):
        self._savedColor = QColorDialog.getColor().name()
        self.__draw_selected_buttons()

    def save_figure_shape(self):
        if len(self._choosenFigureList) == self.MAXIMUM_SIZE and self.centerSheet.is_pressed():
            print('save')
            saved_figure = [
                [single[0] - self.SHIFT_X, single[1] - self.SHIFT_Y]
                for single in self._choosenFigureList
            ]
            Shape.write_figure_data(saved_figure, self._savedColor)

    def __propose_direction(self, to_coordinates):
        propose_move_p = self.__check_figure_propose_move(
            to_coordinates[0], to_coordinates[1]
        )
        print('Propose direction: x: ', to_coordinates[0],' y: ', to_coordinates[1], ' is good: ', propose_move_p)
        if propose_move_p:
            self._proposedFiguresList[-1].append(to_coordinates)
            self._sheet[to_coordinates[1]][to_coordinates[0]].propose_color()

    def __check_figure_propose_move(self, to_x, to_y):
        return self.__check_figure_position(to_x, to_y) and \
               not self._sheet[to_y][to_x].is_pressed()

    def __check_figure_position(self, x, y):
        """
        Check whatever x and y is in bounds of the drawing coordinate

        """
        return 0 <= x < self.MAX_X and 0 <= y < self.MAX_Y

    def __draw_selected_buttons(self):
        for y_c, x_c in self._choosenFigureList:
            self._sheet[x_c][y_c].pressed_color(self._savedColor)

    def take_clicked_frame(self, coordinates):

        if len(self._proposedFiguresList) > 0 and not self._sheet[coordinates[1]][coordinates[0]].is_proposed():
            print('bad direction!')
            return

        # Draw proposed direction (where can move user)
        if len(self._choosenFigureList) != 0:
            self._proposedFiguresList.append([])
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

        if len(self._choosenFigureList) >= self.MAXIMUM_SIZE:
            coord_del_figure = self._choosenFigureList.pop(0)
            self._sheet[coord_del_figure[1]][coord_del_figure[0]].default_color()
            self._sheet[coord_del_figure[1]][coord_del_figure[0]].reset_statement()

        # Clear propose direction
        if len(self._proposedFiguresList) > 1:
            for single_prop in self._proposedFiguresList[0]:
                self._sheet[single_prop[-1]][single_prop[0]].default_color()
                self._sheet[single_prop[-1]][single_prop[0]].reset_statement()
            self._proposedFiguresList.pop(0)

        self._choosenFigureList.append(coordinates[:2])
        self.__draw_selected_buttons()
        print('x: ', coordinates[0], 'y: ', coordinates[1])

