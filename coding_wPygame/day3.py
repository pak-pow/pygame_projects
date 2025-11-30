"""
Today I am going to be learning how to do a keyboard input
amd mouse input and many-many more
"""

import sys
import pygame
from pygame.locals import *

def main():

    # setting up the pygame
    pygame.init()

    # setting up the window
    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 500

    # setting up the display
    DISPLAY = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # setting up our variables
    PLAYER_RECT = pygame.Rect(200,200,50,50)

    # player's movements
    M_left = False
    M_right = False
    M_up = False
    M_down = False

    # speed
    MOVEMENT_SPEED = 1
    BOUNCE = 10  # how strong the bounce is


    # cursor
    mouse_pos = (0,0)
    cursor_color = (255,0,0)

    # Game Loop
    while True:

        for event in pygame.event.get():

            # if the user pressed the X
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:

                # updated the new logic so that if the user preses either arrow keys or
                # WASD it will move
                if event.key == K_LEFT or event.key == K_a:
                    M_left = True

                if event.key == K_RIGHT or event.key == K_d:
                    M_right = True

                if event.key == K_UP or event.key == K_w:
                    M_up = True

                if event.key == K_DOWN or event.key == K_s:
                    M_down = True

                # added a teleportation logic to teleport
                # to the middle of the screen
                if event.key == K_SPACE:
                    PLAYER_RECT.center = (300,250)

            if event.type == KEYUP:

                if event.key == K_LEFT or event.key == K_a:
                    M_left = False

                if event.key == K_RIGHT or event.key == K_d:
                    M_right = False

                if event.key == K_UP or event.key == K_w:
                    M_up = False

                if event.key == K_DOWN or event.key == K_s:
                    M_down = False

            if event.type == MOUSEMOTION:
                # Update tuple (x, y)
                mouse_pos = event.pos

            if event.type == MOUSEBUTTONDOWN:
                cursor_color = (0,255,0)

            elif event.type == MOUSEBUTTONUP:
                cursor_color = (255,0,0)

        # Move player
        if M_left:
            PLAYER_RECT.x -= MOVEMENT_SPEED

        if M_right:
            PLAYER_RECT.x += MOVEMENT_SPEED

        if M_up:
            PLAYER_RECT.y -= MOVEMENT_SPEED

        if M_down:
            PLAYER_RECT.y += MOVEMENT_SPEED

        # --- Bounce Walls ---
        if PLAYER_RECT.left < 0:
            PLAYER_RECT.left = 0
            PLAYER_RECT.x += BOUNCE

        if PLAYER_RECT.right > WINDOW_WIDTH:
            PLAYER_RECT.right = WINDOW_WIDTH
            PLAYER_RECT.x -= BOUNCE

        if PLAYER_RECT.top < 0:
            PLAYER_RECT.top = 0
            PLAYER_RECT.y += BOUNCE

        if PLAYER_RECT.bottom > WINDOW_HEIGHT:
            PLAYER_RECT.bottom = WINDOW_HEIGHT
            PLAYER_RECT.y -= BOUNCE


        DISPLAY.fill((255, 255, 255))
        pygame.draw.rect(DISPLAY, (0, 0, 255), PLAYER_RECT)
        pygame.draw.circle(DISPLAY, cursor_color, mouse_pos, 20)
        pygame.display.update()

if __name__ == "__main__":
    main()