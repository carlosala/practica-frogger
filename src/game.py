"""Main Game class"""

from enum import Enum
from math import floor
from tkinter import Canvas, PhotoImage

from consts import (
    CELL_SIZE,
    HEIGHT_CELLS,
    LOSER_TEXT_COLOR,
    SAFE_CELL_COLOR,
    SEA_CELL_COLOR,
    WIDTH_CELLS,
    WINNER_TEXT_COLOR,
)
from entities.frog import Frog
from entities.lane import Lane, LaneKind


class GameState(Enum):
    """State of the Game"""

    PLAYING = 0
    WON = 1
    LOST = 2


class Game:
    """Complete game class"""

    def __init__(self, win: Canvas, frogs_to_win: int) -> None:
        self.__win = win
        self.__state: GameState = GameState.PLAYING
        self.__frogs_to_win = frogs_to_win
        self.__curr_frog = Frog(win, WIDTH_CELLS / 2, HEIGHT_CELLS - 1)
        self.__won_frogs: list[Frog] = []
        log_lanes = [Lane(win, LaneKind.LOGS, i) for i in range(2, 7)]
        car_lanes = [Lane(win, LaneKind.CARS, i) for i in range(8, 13)]
        self.__lanes = log_lanes + car_lanes
        self.__top_image = PhotoImage(file="assets/checkered.png")

    @property
    def state(self):
        return self.__state

    def __create_new_frog(self) -> None:
        self.__curr_frog = Frog(self.__win, WIDTH_CELLS / 2, HEIGHT_CELLS - 1)

    def __clean_and_print_base(self) -> None:
        self.__win.delete("all")

        # safe zones
        self.__win.create_rectangle(
            0,
            (HEIGHT_CELLS - 1) * CELL_SIZE,
            WIDTH_CELLS * CELL_SIZE,
            HEIGHT_CELLS * CELL_SIZE,
            fill=SAFE_CELL_COLOR,
        )
        self.__win.create_rectangle(
            0,
            floor(HEIGHT_CELLS / 2) * CELL_SIZE,
            WIDTH_CELLS * CELL_SIZE,
            floor(HEIGHT_CELLS / 2 + 1) * CELL_SIZE,
            fill=SAFE_CELL_COLOR,
        )

        # sea zone
        self.__win.create_rectangle(
            0,
            2 * CELL_SIZE,
            WIDTH_CELLS * CELL_SIZE,
            floor(HEIGHT_CELLS / 2) * CELL_SIZE,
            fill=SEA_CELL_COLOR,
        )

        # lane lines
        for i in range(1, 5):
            y = (floor(HEIGHT_CELLS / 2 + 1) + i) * CELL_SIZE
            self.__win.create_line(
                28,
                y,
                WIDTH_CELLS * CELL_SIZE,
                y,
                dash=(100, 26),
                fill="white",
            )

        # screen top
        self.__win.create_image(0, 0, image=self.__top_image, anchor="nw")

    def tick(self, frog_move_x: int, frog_move_y: int) -> None:
        if self.__state != GameState.PLAYING:
            raise Exception("You're not allowed to tick!")
        self.__curr_frog.move(frog_move_x, frog_move_y)
        frog_valid = True
        for lane in self.__lanes:
            lane.tick(self.__curr_frog)
            if lane.y == self.__curr_frog.y:  # will only be executed once per tick
                frog_valid = lane.is_valid_frog(self.__curr_frog)
        if not frog_valid:
            self.__state = GameState.LOST
        # we finished the frog in this case
        if self.__curr_frog.y == 1:
            self.__won_frogs.append(self.__curr_frog)
            if len(self.__won_frogs) >= self.__frogs_to_win:
                self.__state = GameState.WON
            else:
                self.__create_new_frog()

    def draw(self) -> None:
        """Move and display all stuff"""

        self.__clean_and_print_base()
        for lane in self.__lanes:
            lane.draw()
        for old_frog in self.__won_frogs:
            old_frog.draw()
        self.__curr_frog.draw()
        if self.__state == GameState.WON:
            self.__win.create_text(
                CELL_SIZE * WIDTH_CELLS / 2,
                CELL_SIZE * (HEIGHT_CELLS + 1) / 2,
                font="serif 24 bold",
                text="You won! Press <q> to quit",
                fill=WINNER_TEXT_COLOR,
            )
        elif self.__state == GameState.LOST:
            self.__win.create_text(
                CELL_SIZE * WIDTH_CELLS / 2,
                CELL_SIZE * (HEIGHT_CELLS + 1) / 2,
                font="serif 24 bold",
                text="You lost! Press <q> to quit",
                fill=LOSER_TEXT_COLOR,
            )
        self.__win.update()
