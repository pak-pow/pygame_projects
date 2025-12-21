import pygame
import sys

from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((40,40))
        self.image.fill((0,0,255))

        self.rect = self.image.get_rect(center = (400,300))
        self.pos = pygame.Vector2(self.rect.center)
        self.velocity = pygame.Vector2()

        self.max_speed = 300
        self.acceleration = 3000
        self.friction = 0.90
        self.threshold = 20

    def update(self, dt):

        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(0,0)

        if keys[K_w]:
            direction.y -= 1

        if keys[K_s]:
            direction.y += 1

        if keys[K_a]:
            direction.x -= 1

        if keys[K_d]:
            direction.x += 1

        if direction.length_squared() > 0:
            direction.normalize()
            self.velocity += direction * self.acceleration * dt

        else:
            self.velocity *= self.friction

            if self.velocity.length() < self.threshold:
                self.velocity.update(0,0)

        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        self.pos += self.velocity * dt

        self.pos.x = max(20, min(Main.DISPLAY_WIDTH - 20, self.pos.x))
        self.pos.y = max(20, min(Main.DISPLAY_HEIGHT - 20, self.pos.y))

        self.rect.center = round(self.pos)

class Main:

    DISPLAY_WIDTH = 800
    DISPLAY_HEIGHT = 600
    DISPLAY_COLOR = (0,0,0)

    CLOCK = pygame.time.Clock()
    FPS = 60

    def __init__(self):

        pygame.init()
        self.DISPLAY = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
        pygame.display.set_caption("DAY23")

    def run(self):

        while True:
            dt = self.CLOCK.tick(self.FPS) / 1000

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.DISPLAY.fill(self.DISPLAY_COLOR)
            pygame.display.update()

if __name__ == "__main__":
    app = Main()
    app.run()