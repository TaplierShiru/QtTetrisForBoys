from main_window.utils.constans import PATH_TO_FIGURES_DATA, COLOR, COORDS, PATH_TO_DEFAULT_DATA
from .tetris_figures_enum import TetrisFiguresEnum
import random
import json
import copy


class Shape:

    # Different shapes of figures (see axis)
    #                      |
    #        .(-1, 1)      |
    #                      |
    #                      |
    #--------.(-1, 0)------.(0, 0)------------------
    #                      |
    #                      |
    #                      .(0, -1)
    #                      |

    @staticmethod
    def read_default_figure_data():
        with open(PATH_TO_DEFAULT_DATA) as fp:
            data = fp.read()
        return json.loads(data)

    @staticmethod
    def read_figure_data():
        with open(PATH_TO_FIGURES_DATA) as fp:
            data = fp.read()
        return json.loads(data)

    @staticmethod
    def write_figure_data(shape_list: list, color: str):
        current_data = Shape.read_figure_data()
        current_data.update({
            str(len(current_data)): {
                COLOR: color,
                COORDS: shape_list
            }
        })

        with open(PATH_TO_FIGURES_DATA, 'w') as fp:
            json.dump(current_data, fp)

    @staticmethod
    def reset_shape_file_to_default():
        with open(PATH_TO_FIGURES_DATA, 'w') as fp:
            json.dump(Shape.read_default_figure_data(), fp)

    def __init__(self):
        data_js = self.read_figure_data()

        self.COLOR_TABLE = [data_js[name][COLOR] for name in data_js]
        self.TABLE_COORD = [data_js[name][COORDS] for name in data_js]
        self.number_of_figures = len(self.TABLE_COORD) - 1

        self.coords = None
        self.length = 0
        self.pieceShape = TetrisFiguresEnum.NoShape

        self.set_shape(TetrisFiguresEnum.NoShape)
    
    def get_shape(self):
        """
        Return current enum of shape

        """

        return self.pieceShape
    
    def set_shape(self, new_shape):
        """
        Set shape

        """
        table = self.TABLE_COORD[new_shape]
        # add custom size

        self.coords = copy.deepcopy(table)
        self.length = len(self.coords)

        self.pieceShape = new_shape
    
    def set_random_shape(self):
        """
        Set random shape

        """
        self.set_shape(random.randint(1, self.number_of_figures))
    
    def get_x(self, index):
        """
        Return x coordinate in certain index
        
        """

        return self.coords[index][0]
    
    def get_y(self, index):
        """
        Return y coordinate in certain index
        
        """

        return self.coords[index][1]
    
    def set_x(self, index, x):
        """
        Set x coord in certain index

        """
        self.coords[index][0] = x
        
    def set_y(self, index, y):
        """
        Set y coord in certain index

        """
        self.coords[index][1] = y
    
    def min_x(self):
        """
        Return minimum value by x axis

        """

        m = min([single[0] for single in self.coords])

        return m
    
    def max_x(self):
        """
        Return maximum value by x axis

        """

        m = max([single[0] for single in self.coords])

        return m
    
    def min_y(self):
        """
        Return minimum value by y axis

        """

        m = min([single[1] for single in self.coords])

        return m
    
    def max_y(self):
        """
        Return maximum value by y axis

        """

        m = max([single[1] for single in self.coords])

        return m
    
    def rotate_left(self):
        """
        Rotate shape to the left

        """

        if self.pieceShape == TetrisFiguresEnum.SquareShape:
            return self

        result = Shape()
        result.set_shape(self.pieceShape)

        for i in range(result.length):
            result.set_x(i,  self.get_y(i))
            result.set_y(i, -self.get_x(i))

        return result
    
    def rotate_right(self):
        """
        Rotate shape to the right

        """

        if self.pieceShape == TetrisFiguresEnum.SquareShape:
            return self

        result = Shape()
        result.set_shape(self.pieceShape)

        for i in range(result.length):
            result.set_x(i, -self.get_y(i))
            result.set_y(i,  self.get_x(i))

        return result
