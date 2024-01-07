"""Frog class"""

from tkinter import Canvas, PhotoImage

from consts import CELL_SIZE, HEIGHT_CELLS, WIDTH_CELLS


class Frog:
    """Frog class"""

    def __init__(self, win: Canvas, x: float, y: int) -> None:
        self.__win = win
        self.__x = x
        self.__y = y
        self.__image = PhotoImage(file="assets/frog.png")

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def move(self, x: float, y: int) -> None:
        """Move Frog (x,y) cells"""
        x = self.__x + x
        y = self.__y + y
        # only moving if we are inside vertical boundaries
        if 0 <= y < HEIGHT_CELLS:
            # moving to the edge if x is outside of boundaries
            # we take 0.5 since x position of frog is the center of the frog
            if x < 0.5:
                x = 0.5
            elif x > WIDTH_CELLS - 0.5:
                x = WIDTH_CELLS - 0.5
            self.__x = x
            self.__y = y

    def draw(self) -> None:
        """Draw Frog in screen"""
        self.__win.create_image(
            self.__x * CELL_SIZE, self.__y * CELL_SIZE, image=self.__image, anchor="n"
        )
