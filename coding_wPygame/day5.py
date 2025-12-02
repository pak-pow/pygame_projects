"""
DAY 5 - learning how to use sprites
"""
# imports

import pygame
import sys

from pygame.sprite import Sprite
from pygame.time import Clock
from pygame.locals import *


# creating player sprite
class Player(Sprite):

    def __init__(self):

        # initializing the parent class from the SPRITE
        # class in pygame
        super().__init__()

        # creating the user object
        self.PLAYER_OBJ = pygame.Surface((50,50))

        # fill it with this color
        self.PLAYER_OBJ.fill((0,0,255))

        # placing it in a position
        self.PLAYER_RECT = self.PLAYER_OBJ.get_rect()
        self.PLAYER_RECT.center = (300,500)

        # Adding physics to the player object
        self.PLAYER_POS_X = float(self.PLAYER_RECT.x)
        self.SPEED = 300

    # update function for every time a user presses
    def update(self, dt):

        # returns a list of what key is pressed
        keys = pygame.key.get_pressed()

        if (keys[K_LEFT] or keys[K_d]) and self.PLAYER_RECT.left > 0:
            self.PLAYER_POS_X -= self.SPEED * dt

        if (keys[K_RIGHT] or keys[K_a]) and self.PLAYER_RECT.left > 0:
            self.PLAYER_POS_X -= self.SPEED * dt

def main():

    pygame.init()

    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 500

    DISPLAY = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    DISPLAY_COLOR = (255,255,255)

    while True:

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        DISPLAY.fill(DISPLAY_COLOR)
        pygame.display.update()

if __name__ == "__main__":
    main()