import pygame
import sys

from pygame.locals import *

class Main:

    DISPLAY_WIDTH = 1000
    DISPLAY_HEIGHT = 600
    DISPLAY_COLOR = (230,230,230)

    CLOCK = pygame.time.Clock()
    FPS = 60

    def __init__(self):

        pygame.init()
        self.DISPLAY = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
        pygame.display.set_caption("DINO RUSH")

    def run(self):

        while True:

            dt = self.CLOCK.tick(self.FPS) / 1000

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.DISPLAY.fill(self.DISPLAY_COLOR)

            pygame.draw.line(self.DISPLAY, (0,0,0), (0,550), (1000,550), 2)
            pygame.display.update()

if __name__ == "__main__":
    app = Main()
    app.run()