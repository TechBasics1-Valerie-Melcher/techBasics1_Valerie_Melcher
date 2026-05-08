# import turtle
from turtle import *
import random

# initial setup: canvas size
width = 400
height = 400
setup(width, height)

# turn off animation, comment it out to see the drawing process
tracer(0, 0)
# set background color
bgcolor('light blue')  # You can either use color names
# change the color of the lines
color('#673AB7')  # Or Hex Code

# I want to create a checkered board as a base
# first, I will define starting point
square_size = 40
start_x = -160
start_y = 160

# draw 8 rows
for row in range(8):
    # draw 8 columns
    for col in range(8):
        # move turtle
        penup()
        goto(start_x + col * square_size,
             start_y - row * square_size)
        pendown()

        # now that the base is done, I need to alternate the colors
        if (row + col) % 2 == 0:
            fillcolor ("lightblue")
        else:
            fillcolor("white")
        # draw filled square
        begin_fill()

        for i in range (4):
            forward (square_size)
            right(90)
        end_fill()
        hideturtle()

update()



# now I want a chess knight to appear randomly in a different square each time
# First I want to randomize the square it appears in
rand_row = random.randint(0,7)
rand_col = random.randint(0,7)

# Now i need to place the knight in the center of the square so it looks cleaner
knight_x = start_x + (rand_col * square_size) + (square_size / 2)
knight_y = start_y - (rand_row * square_size) - (square_size * 0.1)

penup()
goto(knight_x, knight_y)
color("red")

# now it's time to add the knight symbol
write ("♘", align="center", font=("Arial", 48, "normal"))

hideturtle()
update()
exitonclick()


done()  # important to keep at the end!