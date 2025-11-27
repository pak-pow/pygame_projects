# DAY 1 - Re-Understanding Pygame and its Functions
# Book: Invent Your own computer games with python by Al Sweigart

# Importing the essentials
import pygame , sys
from pygame.locals import *

# initializing the pygame
pygame.init()

# Setting the window into 500 pixels in width and 400 in height
# We store this in the variable 'screen' so we can draw on it later.
screen = pygame.display.set_mode((500, 400))

# Create a Rect object to represent our button.
# Arguments are: (left_x, top_y, width, height)
button_rect = pygame.Rect(100, 100, 200, 50)

# setting the background color of the said rectangle
# Define the initial color to be variable (Red)
color = (255, 0, 0)

# The Game Loop
# This infinite loop runs continuously to keep the game running.
while True:

    # pygame.event.get() grabs a list of all input actions (clicks, keys)
    # that happened since the last frame. We loop through them one by one.
    for event in pygame.event.get():

        # Check if the user clicked the 'X' button on the window
        if event.type == QUIT:

            # Unload pygame modules
            pygame.quit()

            # Close the python script completely
            sys.exit()

        # Check if the user clicked the mouse button AND if the mouse cursor
        # was inside the button's rectangle area.
        if event.type == MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
            print("Button was clicked!")

            # Toggle Logic: Check the *current* color to decide the *next* color.
            # If it is currently Blue...
            if color == (0, 0, 255):

                # ...change it to Red
                color = (255, 0, 0)

            # Otherwise (if it is Red)..
            else:

                # ...change it to Blue
                color = (0, 0, 255)

    # Fill the background with White to erase the previous frame's drawings.
    # Without this, moving objects would leave a "trail".
    screen.fill((255, 255, 255))

    # Draw the button rectangle on the 'screen' surface using the current 'color'.
    pygame.draw.rect(screen, color, button_rect)

    # Set the window title
    pygame.display.set_caption("TEST PYGAME  ")

    # This flips the memory buffer to the actual screen so the user sees the changes.
    pygame.display.update()

