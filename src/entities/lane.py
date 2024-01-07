"""Lane class"""

from enum import Enum
from math import floor
from random import randint, random
from tkinter import Canvas, PhotoImage

from consts import CELL_SIZE, WIDTH_CELLS
from entities.frog import Frog


class LaneKind(Enum):
    """Enum for both kinds of lanes"""

    CARS = 0
    LOGS = 1


class Lane:
    """Lane class"""

    def __init__(self, win: Canvas, kind: LaneKind, y: int) -> None:
        self.__win = win
        self.__kind = kind
        self.__y = y
        # (-0.2, -0.1) u (0.1, 0.2)
        self.__speed = (0.1 + random() * 0.1) * (1 if random() > 0.5 else -1)
        if self.__kind == LaneKind.LOGS:
            self.__entity_width = randint(1, 4)
            self.__image = PhotoImage(file="assets/log.png")
        else:
            image_path = "assets/"
            if random() < 0.25:  # 25% ==> truck (width 2), 75% ==> car (width 1)
                self.__entity_width = 2
                image_path += "truck"
            else:
                self.__entity_width = 1
                image_path += f"car{randint(1, 4)}"
            if self.__speed < 0:
                image_path += "_rotated"
            image_path += ".png"
            self.__image = PhotoImage(file=image_path)
        self.__space = self.__entity_width + 3 + random() * 2  # between 3 and 5 + width
        self.__x = self.__space * random()

    @property
    def y(self):
        return self.__y

    def tick(self, frog: Frog) -> None:
        # we want the center to be between (-space, space)
        self.__x = (self.__x + self.__speed) % self.__space
        if frog.y == self.__y and self.__kind == LaneKind.LOGS:
            frog.move(self.__speed, 0)

    def draw(self) -> None:
        x = self.__x
        if -self.__entity_width / 2 < self.__x - self.__space:
            x = self.__x - self.__space
        while x < WIDTH_CELLS + self.__entity_width / 2:
            if self.__kind == LaneKind.LOGS:
                offset = 1
                if self.__entity_width % 2 == 0:
                    offset = 0.5
                else:
                    # center image if entity_width is odd
                    self.__win.create_image(
                        x * CELL_SIZE,
                        self.__y * CELL_SIZE,
                        image=self.__image,
                        anchor="n",
                    )
                for i in range(floor(self.__entity_width / 2)):
                    self.__win.create_image(
                        (x - i - offset) * CELL_SIZE,
                        self.__y * CELL_SIZE,
                        image=self.__image,
                        anchor="n",
                    )
                    self.__win.create_image(
                        (x + i + offset) * CELL_SIZE,
                        self.__y * CELL_SIZE,
                        image=self.__image,
                        anchor="n",
                    )
                    pass
            else:
                self.__win.create_image(
                    x * CELL_SIZE, self.__y * CELL_SIZE, image=self.__image, anchor="n"
                )
            x += self.__space

    def is_valid_frog(self, frog: Frog) -> bool:
        # frog might be closer to x - space or x + space
        frog_rel_x = frog.x % self.__space
        dist_frog_center = min(
            abs(frog_rel_x - self.__x),
            abs(frog_rel_x - (self.__x - self.__space)),
            abs(frog_rel_x - (self.__x + self.__space)),
        )
        # frog has width 1
        is_touching = dist_frog_center < (self.__entity_width + 1) / 2
        return is_touching if self.__kind == LaneKind.LOGS else not is_touching
