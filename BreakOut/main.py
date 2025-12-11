import pygame
import sys

from pygame.locals import *

class Main:
    def __init__(self):

        pygame.init()

        self.DISPLAY_WIDTH = 800
        self.DISPLAY_HEIGHT = 600
        self.DISPLAY_COLOR = (255,255,255)
        self.DISPLAY = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))

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