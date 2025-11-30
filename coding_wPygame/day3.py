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

    # cursor
    mouse_pos = (0,0)

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

        # --- Game Logic (Movement) ---
        # Move the player if the flags are True
        if M_left and PLAYER_RECT.left > 0:
            PLAYER_RECT.x -= MOVEMENT_SPEED

        if M_right and PLAYER_RECT.right < 600:
            PLAYER_RECT.x += MOVEMENT_SPEED

        if M_up and PLAYER_RECT.top > 0:
            PLAYER_RECT.y -= MOVEMENT_SPEED

        if M_down and PLAYER_RECT.bottom < 500:
            PLAYER_RECT.y += MOVEMENT_SPEED

        DISPLAY.fill((255,255,255))

        # Draw Keyboard Player (Blue Square)
        pygame.draw.rect(DISPLAY, (0, 0, 255), PLAYER_RECT)
        pygame.draw.circle(DISPLAY, (255, 0, 0), mouse_pos, 20)
        pygame.display.update()

if __name__ == "__main__":
    main()