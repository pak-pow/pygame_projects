import pygame
import sys

from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((40,40))
        self.image.fill((0,255,0))

        self.rect = self.image.get_rect(center = (400,300))
        self.pos = pygame.math.Vector2(400,300)

        self.speed = 250

    def update(self, dt):

        keys = pygame.key.get_pressed()
        direction = pygame.math.Vector2(0,0)

        if keys[K_w]:
            direction.y -= 1

        if keys[K_s]:
            direction.y += 1

        if keys[K_a]:
            direction.x -= 1

        if keys[K_d]:
            direction.x += 1

        if direction.length() > 0:
            direction.normalize()

            self.pos += direction * self.speed * dt

        self.pos.x = max(20, min(Main.DISPLAY_WIDTH - 20, self.pos.x))
        self.pos.y = max(20, min(Main.DISPLAY_HEIGHT - 20, self.pos.y))

        self.rect.center = (round(self.pos.x), self.pos.y)

class Main:

    DISPLAY_WIDTH = 800
    DISPLAY_HEIGHT = 600
    DISPLAY_COLOR = (0,0,0)

    def __init__(self):

        pygame.init()
        self.DISPLAY = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))

        self.CLOCK = pygame.time.Clock()
        self.FPS = 60

    def run(self):

        player = Player()
        all_sprite = pygame.sprite.Group(player)

        while True:
            dt = self.CLOCK.tick(self.FPS) / 1000

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            all_sprite.update(dt)
            self.DISPLAY.fill(self.DISPLAY_COLOR)
            pygame.display.set_caption("SPACE INVADERS")

            all_sprite.draw(self.DISPLAY)
            pygame.display.update()

if __name__ == "__main__":
    app = Main()
    app.run()