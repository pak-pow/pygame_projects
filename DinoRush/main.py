import random

import pygame
import sys

from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((30,30))
        self.image.fill((255,0,0))

        self.rect = self.image.get_rect(midbottom = (100, Main.FLOOR_Y))
        self.pos = pygame.Vector2(self.rect.center)
        self.velocity = pygame.Vector2()

        self.on_ground = True
        self.jump_count = 0
        self.max_jump = 2

    def jump(self):

        if self.jump_count < self.max_jump:
            self.velocity.y = Main.JUMP_STRENGTH
            self.jump_count += 1
            self.on_ground = False

    def update(self, dt):

        keys = pygame.key.get_pressed()
        current_gravity = Main.GRAVITY

        if keys[K_s]:
            current_gravity += 4000

        self.velocity.y += current_gravity * dt
        self.pos += self.velocity * dt

        if self.pos.y >= Main.FLOOR_Y:
            self.pos.y = Main.FLOOR_Y

            self.velocity.y = 0
            self.on_ground = True
            self.jump_count = 0

        self.rect.midbottom = round(self.pos.x), round(self.pos.y)

class Cactus(pygame.sprite.Sprite):
    def __init__(self, x_offset = 0):
        super().__init__()

        width = random.randint(20,35)
        height = random.randint(40,70)

        self.image = pygame.Surface((width,height))
        self.image.fill((0,150,0))

        spawn_x = Main.DISPLAY_WIDTH + 40 + x_offset
        self.rect = self.image.get_rect(bottomleft = (spawn_x  + 50, Main.FLOOR_Y))
        self.pos = pygame.Vector2(self.rect.topleft)

    def update(self, dt):

        self.pos.x -= Main.MOVE_SPEED * dt
        self.rect.x = round(self.pos.x)

        if self.rect.x < 0:
            self.kill()

class Main:

    DISPLAY_WIDTH = 1000
    DISPLAY_HEIGHT = 600
    DISPLAY_COLOR = (230,230,230)

    CLOCK = pygame.time.Clock()
    FPS = 60

    GRAVITY = 2000
    JUMP_STRENGTH = - 800
    MOVE_SPEED = 800
    FLOOR_Y = 550

    def __init__(self):

        pygame.init()
        self.DISPLAY = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
        pygame.display.set_caption("DINO RUSH")

    def run(self):

        all_sprites = pygame.sprite.Group()
        player = Player()

        all_sprites.add(player)

        while True:

            dt = self.CLOCK.tick(self.FPS) / 1000

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        player.jump()

            all_sprites.update(dt)
            self.DISPLAY.fill(self.DISPLAY_COLOR)

            all_sprites.draw(self.DISPLAY)
            pygame.draw.line(self.DISPLAY, (0,0,0), (0,550), (1000,550), 2)
            pygame.display.update()

if __name__ == "__main__":
    app = Main()
    app.run()