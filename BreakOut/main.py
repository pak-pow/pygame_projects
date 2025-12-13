import pygame
import sys

from pygame.locals import *


LEVEL_MAP = [
    "XXXXXXXXXXXXXXX",  # 0  Top wall
    "XBBBBBBBBBBBBBX",  # 1
    "XBBBBBBBBBBBBBX",  # 2
    "XBBBBBBBBBBBBBX",  # 3
    "XBBBBBBBBBBBBBX",  # 4
    "XBBBBBBBBBBBBBX",  # 5
    "X             X",  # 6
    "X             X",  # 7
    "X             X",  # 8
    "X             X",  # 9
    "X             X",  # 10
    "X             X",  # 11
    "X             X",  # 12
    "X             X",  # 13
    "X             X",  # 14
    "X             X",  # 15
    "X      O      X",  # 16 Ball spawn
    "X             X",  # 17
    "X    PPPPP    X",  # 18 Paddle
    "XXXXXXXXXXXXXXX",  # 19 Bottom wall
]


class Tile(pygame.sprite.Sprite):

    def __init__(self, pos, type):
        super().__init__()

        self.image = pygame.Surface((Main.TILE_SIZE, Main.TILE_SIZE))

        if type == "X":
            self.image.fill((180,180,180))
            pygame.draw.rect(
                self.image,
                (80,80,80),
                (0,0, Main.TILE_SIZE, Main.TILE_SIZE),
                3
            )

        elif type == "B":
            self.image.fill((0,150,255))
            pygame.draw.rect(
                self.image,
                (0,80,250),
                self.image.get_rect(),
                2
            )

        elif type == "P":
            self.image.fill((0,255,0))

        elif type == "O":
            self.image.fill((255,255,0))

        else:
            self.kill()




class Main:

    TILE_SIZE = 40
    DISPLAY_WIDTH = 600
    DISPLAY_HEIGHT = 800
    DISPLAY_COLOR = (0,0,0)
    DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

    def __init__(self):

        pygame.init()
        self.CLOCK = pygame.time.Clock()
        self.FPS = 60

    def run(self):

        while True:

            dt = self.CLOCK.tick(self.FPS) / 1000

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.DISPLAY.fill(self.DISPLAY_COLOR)

            pygame.display.set_caption("BreakOut")
            pygame.display.update()

if __name__ == "__main__":
    app = Main()
    app.run()