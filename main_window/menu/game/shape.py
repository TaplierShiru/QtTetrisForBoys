from .tetrominoe import Tetrominoe
import random



class Shape:

    # Different shapes of figures (see axis)
    #              |
    #    .(-1, 1)  |
    #              |
    #              |
    #----.(-1, 0)--.(0, 0)------------------
    #              |
    #              |
    #              .(0, -1)
    #              |
    TABLE_COORD = (
        ((0, 0), (0, 0), (0, 0), (0, 0)),
        ((0, -1), (0, 0), (-1, 0), (-1, 1)),
        ((0, -1), (0, 0), (1, 0), (1, 1)),
        ((0, -1), (0, 0), (0, 1), (0, 2)),
        ((-1, 0), (0, 0), (1, 0), (0, 1)),
        ((0, 0), (1, 0), (0, 1), (1, 1)),
        ((-1, -1), (0, -1), (0, 0), (0, 1)),
        ((1, -1), (0, -1), (0, 0), (0, 1))
    )

    COLOR_TABLE = [
        0x000000, 
        0xCC6666, 
        0x66CC66, 
        0x6666CC,
        0xCCCC66, 
        0xCC66CC, 
        0x66CCCC, 
        0xDAAA00       
    ]


    def __init__(self):

        self.coords = [[0, 0] for _ in range(4)]
        self.pieceShape = Tetrominoe.NoShape

        self.set_shape(Tetrominoe.NoShape)
    
    def get_shape(self):
        """
        Return current enum of shape

        """

        return self.pieceShape
    
    def set_shape(self, new_shape):
        """
        Set shape

        """

        table = Shape.TABLE_COORD[new_shape]
        for i in range(4):
            for j in range(2):
                self.coords[i][j] = table[i][j]
        self.pieceShape = new_shape
    
    def set_random_shape(self):
        """
        Set random shape

        """
        self.set_shape(random.randint(1, 7))
    
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

        if self.pieceShape == Tetrominoe.SquareShape:
            return self

        result = Shape()
        result.pieceShape = self.pieceShape

        for i in range(4):
            result.set_x(i, self.get_y(i))
            result.set_y(i, -self.get_x(i))

        return result
        
    
    def rotate_right(self):
        """
        Rotate shape to the right

        """

        if self.pieceShape == Tetrominoe.SquareShape:
            return self

        result = Shape()
        result.pieceShape = self.pieceShape

        for i in range(4):
            result.set_x(i, -self.get_y(i))
            result.set_y(i, self.get_x(i))

        return result     
    
