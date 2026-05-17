# ----------------------------------------
# Assignment 5 - Refactored Chess Board
# ----------------------------------------

from turtle import *
import random

# -----------------------------
# Constants / Global Variables
# -----------------------------

window_width = 400
window_height = 400

board_size = 8
square_size = 40

start_x = -160
start_y = 160

first_color = "lightblue"
second_color = "white"
knight_color = "red"

background_color = "light blue"


# -----------------------------
# Setup Functions
# -----------------------------

def setup_screen():
    """
    Set up the turtle screen and drawing settings.
    """
    setup(window_width, window_height)
    bgcolor(background_color)

    tracer(0, 0)  # To turn off animation
    color("#673AB7")


# -----------------------------
# Drawing Functions
# -----------------------------

def draw_square(x, y, square_color):
    """
    I'm starting by drawing one filled square at position (x, y).
    """
    penup()
    goto(x, y)
    pendown()

    fillcolor(square_color)

    begin_fill()

    for _ in range(4):
        forward(square_size)
        right(90)

    end_fill()


def draw_board():
    """
    Now I will draw the full 8x8 chess board.
    """
    for row in range(board_size):

        for col in range(board_size):

            # Calculate square position
            x = start_x + col * square_size
            y = start_y - row * square_size

            # Alternate colors
            if (row + col) % 2 == 0:
                square_color = first_color
            else:
                square_color = second_color

            draw_square(x, y, square_color)


# -----------------------------
# Knight Functions
# -----------------------------

def get_random_position():
    """
    I want the knight to appear in a random row and column.
    Returns:
        tuple: (row, col)
    """
    row = random.randint(0, board_size - 1)
    col = random.randint(0, board_size - 1)

    return row, col


def draw_knight(row, col):
    """
    The knight is supposed to appear in the center of the square.
    """
    knight_x = start_x + (col * square_size) + (square_size / 2)
    knight_y = start_y - (row * square_size) - (square_size * 0.1)

    penup()
    goto(knight_x, knight_y)

    color(knight_color)

    write("♘", align="center", font=("Arial", 48, "normal"))


# -----------------------------
# Main Function
# -----------------------------

def main():
    """
    This is where I will now execute my generative art.
    """

    setup_screen()

    draw_board()

    # Generate random knight position
    random_row, random_col = get_random_position()

    # Draw knight
    draw_knight(random_row, random_col)

    hideturtle()

    update()

    exitonclick()


# Run the program
main()

done()
