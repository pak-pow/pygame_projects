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
    MOVE_SPEED = 800
    FLOOR_Y = 600
    DISPLAY_WIDTH = 800
    DISPLAY_HEIGHT = 600

    def __init__(self):

        pygame.init()
        self.DISPLAY = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))

        self.CLOCK = Clock()
        self.FPS = 60

        self.player = Player()
        self.all_sprites = pygame.sprite.Group(self.player)

    def run(self):

        while True:

            dt = self.CLOCK.tick(self.FPS) / 1000

            for event in pygame.event.get():

                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.player.jump()

            self.all_sprites.update(dt)

            self.DISPLAY.fill(self.UI_BLACK)
            self.all_sprites.draw(self.DISPLAY)

            pygame.display.set_caption("DAY9: GRAVITY")
            pygame.display.update()


class Player(Sprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((50,50))
        self.image.fill(Main.UI_WHITE)
        self.rect = self.image.get_rect(midbottom = (400, Main.FLOOR_Y))

        self.pos = Vector2(400, Main.FLOOR_Y)
        self.velocity = Vector2(0,0)

        self.on_ground = True
        self.jump_count = 0
        self.max_jump = 2

    def jump(self):

        if self.jump_count < self.max_jump:
            self.velocity.y = Main.JUMP_STRENGTH
            self.jump_count += 1

    def update(self, dt):

        keys = pygame.key.get_pressed()

        self.velocity.x = 0

        if keys[K_LEFT] or keys[K_a]:
            self.velocity.x = -Main.MOVE_SPEED

        if keys[K_RIGHT] or keys[K_d]:
            self.velocity.x = Main.MOVE_SPEED

        self.velocity.y += Main.GRAVITY * dt
        self.pos += self.velocity * dt

        if self.pos.y >= Main.FLOOR_Y:
            self.pos.y = Main.FLOOR_Y
            self.velocity.y = 0
            self.on_ground = True
            self.jump_count = 0

        else:
            self.on_ground = False

        if self.pos.x <= 25:
            self.pos.x = 25
            self.jump_count = 0

        if self.pos.x >= Main.DISPLAY_WIDTH - 25:
            self.pos.x = Main.DISPLAY_WIDTH - 25
            self.jump_count = 0

        self.rect.midbottom = round(self.pos)

if __name__ == "__main__":
    app = Main()
    app.run()