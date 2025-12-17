import pygame
import sys

from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self, all_sprites, bullet_group):
        super().__init__()

        self.image = pygame.Surface((40,40))
        self.image.fill((0,255,0))

        self.rect = self.image.get_rect(center = (400,500))
        self.pos = pygame.math.Vector2(self.rect.center)

        self.speed = 250
        self.last_shot_time = 0
        self.shoot_delay = 250

        self.all_sprites = all_sprites
        self.bullet_group = bullet_group


    def shoot(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_shot_time >= self.shoot_delay:
            self.last_shot_time = current_time

            bullet = Bullet(self.rect.midtop)
            self.bullet_group.add(bullet)
            self.all_sprites.add(bullet)

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[K_a]:
            self.pos.x -= self.speed * dt
        if keys[K_d]:
            self.pos.x += self.speed * dt

        if keys[K_SPACE]:
            self.shoot()

        self.pos.x = max(20, min(Main.DISPLAY_WIDTH - 20, self.pos.x))
        self.rect.centerx = (round(self.pos.x))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_pos):
        super().__init__()

        self.image = pygame.Surface((6, 14))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(midbottom = start_pos)

        self.speed = 600

    def update(self, dt):
        self.rect.y -= self.speed * dt

        if self.rect.bottom < 0:
            self.kill()


class Main:

    DISPLAY_WIDTH = 800
    DISPLAY_HEIGHT = 600
    DISPLAY_COLOR = (0,0,0)

    def __init__(self):

        pygame.init()
        self.DISPLAY = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))

        pygame.display.set_caption("SPACE INVADERS")
        self.CLOCK = pygame.time.Clock()
        self.FPS = 60

    def run(self):
        all_sprites = pygame.sprite.Group()
        bullet_group = pygame.sprite.Group()

        player = Player(all_sprites, bullet_group)
        all_sprites.add(player)

        while True:
            dt = self.CLOCK.tick(self.FPS) / 1000

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            all_sprites.update(dt)
            self.DISPLAY.fill(self.DISPLAY_COLOR)

            all_sprites.draw(self.DISPLAY)
            pygame.display.update()

if __name__ == "__main__":
    app = Main()
    app.run()