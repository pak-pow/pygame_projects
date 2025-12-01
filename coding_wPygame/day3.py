"""
Day 3 - Keyboard & Mouse Input + Bounce Movement
Today I learned how to detect key presses, key releases,
mouse movement, mouse clicks, and how to move a square on screen.
"""

import sys
import pygame
from pygame.locals import *

def main():

    # initializing pygame, this has to be called before anything else
    pygame.init()

    # basically my window setup
    # width = 600, height = 500
    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 500
    DISPLAY = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # this is my blue square (player)
    # it starts at x = 200, y = 200 and is 50x50 in size
    PLAYER_RECT = pygame.Rect(200,200,50,50)

    # these booleans are like switches I turn ON/OFF depending on
    # what keys I'm pressing. I use them later to move the square.
    M_left = False
    M_right = False
    M_up = False
    M_down = False

    # how fast the player moves per frame
    MOVEMENT_SPEED = 1

    # how strong the bounce is when the square hits a wall
    # (this is just my own idea to make it bounce back)
    BOUNCE = 10

    # mouse related variables
    # mouse_pos tracks where my mouse currently is
    # cursor_color changes depending on if I'm clicking or not
    mouse_pos = (0,0)
    cursor_color = (255,0,0)

    # the game loop, this is what keeps everything running forever
    while True:

        # event handling section
        # this checks every little thing the user does (keyboard, mouse, quit)
        for event in pygame.event.get():

            # if the user presses the close button, quit the whole program
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # runs only ONCE when I initially press a key
            if event.type == KEYDOWN:

                # turning on the movement booleans (this means I'm holding the key)
                if event.key == K_LEFT or event.key == K_a:
                    M_left = True

                if event.key == K_RIGHT or event.key == K_d:
                    M_right = True

                if event.key == K_UP or event.key == K_w:
                    M_up = True

                if event.key == K_DOWN or event.key == K_s:
                    M_down = True

                # spacebar instantly teleports the square to the center
                # I'm adding this as a fun mechanic to test input
                if event.key == K_SPACE:
                    PLAYER_RECT.center = (300,250)

            # runs only ONCE when I release the key
            # this stops the movement in that direction
            if event.type == KEYUP:

                if event.key == K_LEFT or event.key == K_a:
                    M_left = False

                if event.key == K_RIGHT or event.key == K_d:
                    M_right = False

                if event.key == K_UP or event.key == K_w:
                    M_up = False

                if event.key == K_DOWN or event.key == K_s:
                    M_down = False

            # when I move the mouse, I store its current position

            if event.type == MOUSEMOTION:
                # Update tuple (x, y)
                mouse_pos = event.pos

            # clicking the mouse button turns the circle green
            if event.type == MOUSEBUTTONDOWN:
                cursor_color = (0,255,0)

            # releasing the mouse button makes it red again
            elif event.type == MOUSEBUTTONUP:
                cursor_color = (255,0,0)


        # ================================================================
        # MOVEMENT LOGIC (This part actually moves the square every frame)
        # ================================================================

        # if a direction flag is ON, move the square a little bit
        # I keep movement outside the event loop so it feels smooth
        if M_left:
            PLAYER_RECT.x -= MOVEMENT_SPEED

        if M_right:
            PLAYER_RECT.x += MOVEMENT_SPEED

        if M_up:
            PLAYER_RECT.y -= MOVEMENT_SPEED

        if M_down:
            PLAYER_RECT.y += MOVEMENT_SPEED

        # ================================================================
        # BOUNCE LOGIC (my own simple bounce system)
        # idea: if the square hits the border, push it back inside
        # ================================================================

        # hitting the left wall
        if PLAYER_RECT.left < 0:

            # make sure it doesn't go offscreen
            PLAYER_RECT.left = 0

            # push it away from the wall
            PLAYER_RECT.x += BOUNCE

        # hitting the right wall
        if PLAYER_RECT.right > WINDOW_WIDTH:
            PLAYER_RECT.right = WINDOW_WIDTH
            PLAYER_RECT.x -= BOUNCE

        # hitting the top wall
        if PLAYER_RECT.top < 0:
            PLAYER_RECT.top = 0
            PLAYER_RECT.y += BOUNCE

        # hitting the bottom wall
        if PLAYER_RECT.bottom > WINDOW_HEIGHT:
            PLAYER_RECT.bottom = WINDOW_HEIGHT
            PLAYER_RECT.y -= BOUNCE

        # ================================================================
        # DRAWING SECTION
        # This is where all visual things are drawn every frame
        # ================================================================

        # clear the screen to white
        DISPLAY.fill((255, 255, 255))

        # the blue square
        pygame.draw.rect(DISPLAY, (0, 0, 255), PLAYER_RECT)

        # circle that follows the mouse
        pygame.draw.circle(DISPLAY, cursor_color, mouse_pos, 20)

        # refresh the screen so we can see everything
        pygame.display.update()

# program starts here
if __name__ == "__main__":
    main()