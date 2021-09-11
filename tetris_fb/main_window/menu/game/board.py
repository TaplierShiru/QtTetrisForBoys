from .shape import Shape
from .tetrominoe import Tetrominoe

from PySide6.QtCore import Qt, QBasicTimer, Signal
from PySide6.QtGui import QPainter, QColor, QBrush
from PySide6.QtWidgets import QFrame


class Board(QFrame):

    msg2StatusBar = Signal(str)

    BOARD_SPEED = 'board_speed'
    BOARD_SIZE = 'board_size'

    def __init__(self, parent, board_width=10, board_height=22, speed=100):
        super().__init__(parent)

        self._board_width = board_width
        self._board_height = board_height
        self._speed = speed

        self.initBoard()
    
    def initBoard(self):
        """
        Init board

        """
        
        # This type of timer is much faster (i.e. more low-lvl) than QTimer
        self.timer = QBasicTimer()
        self.isWaitingAfterLine = False

        self.curX = 0
        self.curY = 0
        self.numLinesRemoved = 0
        self.board = []

        self.setFocusPolicy(Qt.StrongFocus)
        self.isStarted = False
        self.isPaused = False
        self.clearBoard()
    
    def shapeAt(self, x, y):
        """
        Datermines shape at the boards position

        """
        return self.board[(y * self._board_width) + x]
    
    def set_shape_at(self, x, y, shape):
        """
        Set shape for certain position

        """

        self.board[(y * self._board_width) + x] = shape
    
    def get_square_width(self):
        """
        Return width of one square

        """

        return self.contentsRect().width() // self._board_width
    
    def get_square_height(self):
        """
        Return height of one square

        """

        return self.contentsRect().height() // self._board_height
    
    def start(self):
        """
        Begin game

        """

        if self.isPaused:
            return
        
        self.isStarted = True
        self.isWaitingAfterLine = True
        self.numLinesRemoved = 0
        self.clearBoard()

        self.msg2StatusBar.emit(str(self.numLinesRemoved))

        self.newPiece()
        self.timer.start(self._speed, self)
    
    def pause(self):
        """
        Set game to pause

        """
        
        if not self.isStarted:
            return
        
        self.isPaused = not self.isPaused

        if self.isPaused:
            self.timer.stop()
            self.msg2StatusBar.emit('Paused')
        else:
            self.timer.start(self._speed, self)
            self.msg2StatusBar.emit(str(self.numLinesRemoved))
        
        self.update()
    
    def paintEvent(self, event: QFrame.paintEvent):
        """
        Paint all shapes of the game

        """
        painter = QPainter(self)
        rect = self.contentsRect()
        #painter.begin(self)
        boardTop = rect.bottom() - self._board_height * self.get_square_height()

        self.drawGameBox(painter)

        for i in range(self._board_height):
            for j in range(self._board_width):
                shape = self.shapeAt(j, self._board_height - i - 1)

                if shape != Tetrominoe.NoShape:
                    self.drawSquare(
                        painter, rect.left() + j * self.get_square_width(),
                        boardTop + i * self.get_square_height(),
                        shape
                    )
        
        if self.curPiece.get_shape() != Tetrominoe.NoShape:

            for i in range(self.curPiece.length):
                x = self.curX + self.curPiece.get_x(i)
                y = self.curY - self.curPiece.get_y(i)
                self.drawSquare(
                    painter,
                    rect.left() + x * self.get_square_width(),
                    boardTop + (self._board_height - y - 1) * self.get_square_height(),
                    self.curPiece.get_shape()
                )
        
        #painter.end()
    
    def keyPressEvent(self, event: QFrame.keyPressEvent):
        """
        Process key pressed event

        """

        if not self.isStarted or self.curPiece.get_shape() == Tetrominoe.NoShape:
            super(Board, self).keyPressEvent(event)
            return
        
        key = event.key()

        if key == Qt.Key_P:
            self.pause()
            return
        
        if self.isPaused:
            return
        
        if key == Qt.Key_Left:
            self.tryMove(self.curPiece, self.curX - 1, self.curY)
        elif key == Qt.Key_Right:
            self.tryMove(self.curPiece, self.curX + 1, self.curY)
        elif key == Qt.Key_Down:
            self.tryMove(self.curPiece.rotate_left(), self.curX, self.curY)
        elif key == Qt.Key_Up:
            self.tryMove(self.curPiece.rotate_right(), self.curX, self.curY)
        elif key == Qt.Key_Space:
            self.dropDown()
        elif key == Qt.Key_D:
            self.oneLineDown()
        else:
            super(Board, self).keyPressEvent(event)
        
    def timerEvent(self, event: QFrame.timerEvent):
        """
        Handle timer events
        
        """
        if event.timerId() == self.timer.timerId():
            if self.isWaitingAfterLine:
                self.isWaitingAfterLine = False
                self.newPiece()
            else:
                self.oneLineDown()
        else:
            super(Board, self).timerEvent(event)
    
    def clearBoard(self):
        """
        Clear shaped on the board

        """
        self.board.clear()
        for _ in range(self._board_height * self._board_width):
            self.board.append(Tetrominoe.NoShape)
        
    def dropDown(self):
        """
        Drop down a shape

        """

        newY = self.curY

        while newY > 0:

            if not self.tryMove(self.curPiece, self.curX, newY - 1):
                break
            
            newY -= 1
        
        self.pieceDropped()
    
    def oneLineDown(self):
        """
        Goes one line down with the shape

        """

        if not self.tryMove(self.curPiece, self.curX, self.curY - 1):
            self.pieceDropped()

    def pieceDropped(self):
        """
        After dropping the shape,
        remove full lines and create new shape

        """

        for i in range(self.curPiece.length):

            x = self.curX + self.curPiece.get_x(i)
            y = self.curY - self.curPiece.get_y(i)
            self.set_shape_at(x, y, self.curPiece.get_shape())
        
        self.removeFullLines()
    
        if not self.isWaitingAfterLine:
            self.newPiece()
        
    def removeFullLines(self):
        """
        Remove all full lines from the board

        """

        numFullLines = 0
        rowsToRemove = []

        for i in range(self._board_height):
            n = 0

            for j in range(self._board_width):
                if not self.shapeAt(j, i) == Tetrominoe.NoShape:
                    n += 1
            
            if n == 10:
                rowsToRemove.append(i)
        
        rowsToRemove.reverse()

        for m in rowsToRemove:

            for k in range(m, self._board_height - 1):
                for i in range(self._board_width):
                    self.set_shape_at(i, k, self.shapeAt(i, k + 1))
        
        numFullLines += len(rowsToRemove)

        if numFullLines > 0:
            self.numLinesRemoved += numFullLines
            self.msg2StatusBar.emit(str(self.numLinesRemoved))

            self.isWaitingAfterLine = True
            self.curPiece.set_shape(Tetrominoe.NoShape)
            self.update()
    
    def newPiece(self):
        """
        Create a new shape

        """

        self.curPiece = Shape()
        self.curPiece.set_random_shape()
        self.curX = self._board_width // 2 + 1
        self.curY = self._board_height - 1 + self.curPiece.min_y()

        if not self.tryMove(self.curPiece, self.curX, self.curY):
            self.curPiece.set_shape(Tetrominoe.NoShape)
            self.timer.stop()
            self.isStarted = False
            self.msg2StatusBar.emit("Game over!")
    
    def tryMove(self, newPiece, newX, newY):
        """
        Tries to move a shape

        """

        for i in range(newPiece.length):

            x = newX + newPiece.get_x(i)
            y = newY - newPiece.get_y(i)

            if x < 0 or x >= self._board_width or y < 0 or y >= self._board_height:
                return False
            
            if self.shapeAt(x, y) != Tetrominoe.NoShape:
                return False
        
        self.curPiece = newPiece
        self.curX = newX
        self.curY = newY
        self.update()

        return True
    
    def drawSquare(self, painter, x, y, shape):
        """

        Draws a square of a shape

        """

        color = self.curPiece.COLOR_TABLE

        color = QColor(color[shape])
        painter.fillRect(
            x + 1, y + 1, 
            self.get_square_width() - 2, self.get_square_height() - 2,
            color
        )

        painter.setPen(color.lighter())
        painter.drawLine(x, y + self.get_square_height() - 1, x, y)
        painter.drawLine(x, y, x + self.get_square_width() - 1, y)

        painter.setPen(color.darker())
        painter.drawLine(
            x + 1, y + self.get_square_height() - 1,
            x + self.get_square_width() - 1, y + self.get_square_height() - 1)

        painter.drawLine(
            x + self.get_square_width() - 1, y + self.get_square_height() - 1,
            x + self.get_square_width() - 1, y + 1
        )

    def drawGameBox(self, painter):
        """
        Draw game box for the widget

        """
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(QColor(255, 0, 0))
        painter.setBrush(brush)

        rect = self.contentsRect()
        painter.drawLine(
            0, 0, 
            rect.width() - 1, 0
        )

        painter.drawLine(
            rect.width() - 1, 0, 
            rect.width() - 1, rect.height() - 1
        )
        
        painter.drawLine(
            rect.width() - 1, rect.height() - 1,
            0, rect.height()
        )

        painter.drawLine(
            0, rect.height() - 1,
            0, 0
        )
