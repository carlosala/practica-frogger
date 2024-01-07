"""Frogger main file"""

from time import sleep
from tkinter import Canvas, Tk

from consts import CELL_SIZE, HEIGHT_CELLS, WIDTH_CELLS
from game import Game, GameState
from keyboard import is_pressed


def main() -> None:
    """Run Frogger game"""

    # get the frogs to win
    frogs_to_win = 3
    while True:
        input_str = input("Enter the amount of frogs to win the game (default 3): ")
        if input_str == "":
            break
        if input_str.isdigit():
            frogs_to_win = int(input_str)
            break

    # init tkinter related stuff
    tk = Tk()
    tk.title("Frogger")
    win = Canvas(
        tk, width=WIDTH_CELLS * CELL_SIZE, height=HEIGHT_CELLS * CELL_SIZE, bg="gray16"
    )
    win.pack()

    # init game
    game = Game(win, frogs_to_win)
    frog_blocked = 0
    while True:
        if is_pressed("q"):
            break
        if game.state == GameState.PLAYING:
            x = 0
            y = 0
            if frog_blocked == 0:
                if is_pressed("right arrow") or is_pressed("d"):
                    x = 1
                if is_pressed("left arrow") or is_pressed("a"):
                    x = -1
                if is_pressed("up arrow") or is_pressed("w"):
                    y = -1
                if is_pressed("down arrow") or is_pressed("s"):
                    y = 1
                if x or y:
                    frog_blocked = 3
            else:
                frog_blocked -= 1
            game.tick(x, y)
            game.draw()
        sleep(0.05)


if __name__ == "__main__":
    main()
