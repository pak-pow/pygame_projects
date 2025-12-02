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
        self.image = pygame.Surface((50,50))

        # fill it with this color
        self.image.fill((0,0,255))

        # placing it in a position
        self.rect = self.image.get_rect()
        self.rect.center = (300,500)

        # Adding physics to the player object
        self.PLAYER_POS_X = float(self.rect.x)
        self.SPEED = 300

    # update function for every time a user presses
    def update(self, dt):

        # returns a list of what key is pressed
        keys = pygame.key.get_pressed()

        if (keys[K_LEFT] or keys[K_a]) and self.rect.left > 0:
            self.PLAYER_POS_X -= self.SPEED * dt

        if (keys[K_RIGHT] or keys[K_d]) and self.rect.right < 600:
            self.PLAYER_POS_X += self.SPEED * dt

        self.rect.x = int(self.PLAYER_POS_X)

class Ball(Sprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((20,20))
        self.image.fill((0,255,0))

        self.rect = self.image.get_rect()
        self.rect.center = (300,200)

        self.VELOCITY_X = 200
        self.VELOCITY_Y = 200

        self.BALL_POSS_X = float(self.rect.x)
        self.BALL_POSS_Y = float(self.rect.y)

    def update(self, dt):

        self.BALL_POSS_X += self.VELOCITY_X * dt
        self.BALL_POSS_Y += self.VELOCITY_Y * dt

        if self.BALL_POSS_X <= 0 or self.BALL_POSS_X >= 580:
            self.VELOCITY_X *= -1

        if self.BALL_POSS_Y <= 0 or self.BALL_POSS_Y >= 480:
            self.VELOCITY_Y *= -1

        self.rect.x = int(self.BALL_POSS_X)
        self.rect.y = int(self.BALL_POSS_Y)

def main():

    pygame.init()
    clock = Clock()
    FPS = 60
    font = pygame.font.SysFont(None, 32)

    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 500

    DISPLAY = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    DISPLAY_COLOR = (255,255,255)

    player = Player()
    ball = Ball()

    all_sprite = pygame.sprite.Group()
    all_sprite.add(player)
    all_sprite.add(ball)

    while True:

        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        all_sprite.update(dt)

        DISPLAY.fill(DISPLAY_COLOR)
        all_sprite.draw(DISPLAY)

        text_surface = font.render(f"FPS: {int(clock.get_fps())}", True, (0, 0, 0))
        DISPLAY.blit(text_surface, (10,10))

        pygame.display.update()

if __name__ == "__main__":
    main()