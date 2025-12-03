"""
DAY 6 about collisions and shit
"""

# imports
import pygame
import sys
import random

from pygame.sprite import Sprite
from pygame.time import Clock
from pygame.locals import *

class Player(Sprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((100,100))
        self.image.fill((0,0,255))
        self.rect = self.image.get_rect(center = (300,200))

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.center = pos

def main():

    pygame.init()

    DISPLAY_WIDTH = 600
    DISPLAY_HEIGHT = 500
    DISPLAY_COLOR = (255,255,255)
    DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

    CLOCK = Clock()
    FPS = 60

    all_sprites = pygame.sprite.Group()

    player = Player()

    all_sprites.add(player)
    while True:

        dt = CLOCK.tick(FPS) / 1000

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()


        DISPLAY.fill(DISPLAY_COLOR)
        all_sprites.draw(DISPLAY)
        pygame.display.update()

if __name__ == "__main__":
    main()