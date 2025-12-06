import pygame
import sys

from pygame.locals import *
from pygame.sprite import Sprite
from pygame.time import Clock
from pygame.math import Vector2

class Main:

    UI_WHITE = (245, 245, 245)
    UI_LIGHT_GRAY = (230, 230, 230)
    UI_GRAY = (180, 180, 180)
    UI_DARK_GRAY = (100, 100, 100)
    UI_BLACK = (20, 20, 20)

    UI_SKY_BLUE = (93, 173, 226)
    UI_NAVY_BLUE = (52, 73, 94)
    UI_PURPLE = (155, 89, 182)
    UI_GREEN = (46, 204, 113)
    UI_ORANGE = (243, 156, 18)
    UI_RED = (231, 76, 60)

    GRAVITY = 2000
    JUMP_STRENGTH = -800
    MOVE_SPEED = 400
    FLOOR_Y = 500

    def __init__(self):

        pygame.init()

        self.DISPLAY_WIDTH = 800
        self.DISPLAY_HEIGHT = 600
        self.DISPLAY = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))

        self.CLOCK = Clock()
        self.FPS = 60

    def run(self):

        while True:

            dt = self.CLOCK.tick(self.FPS) / 1000

            for event in pygame.event.get():

                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.DISPLAY.fill(self.UI_BLACK)
            pygame.display.set_caption("DAY9: GRAVITY")
            pygame.display.update()


class Player(Sprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((50,50))
        self.image.fill(Main.UI_WHITE)
        self.rect = self.image.get_rect(midbottom = (400, Main.FLOOR_Y))
        self.pos = Vector2(0,0)

    def update(self, dt):
        pass

if __name__ == "__main__":
    app = Main()
    app.run()