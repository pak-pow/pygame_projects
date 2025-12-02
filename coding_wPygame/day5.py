"""
DAY 5 - learning how to use sprites
"""
from symtable import Class

# imports

import pygame
import sys

from pygame.sprite import Sprite
from pygame.time import Clock
from pygame.locals import *


# creating player sprite
class Player(Sprite):

    def __init__(self):
        super().__init__()

    pass

def main():

    pygame.init()

    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 500
    DISPLAY = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

    while True:

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        DISPLAY.fill((255,255,255))
        pygame.display.update()

if __name__ == "__main__":
    main()