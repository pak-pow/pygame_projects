import pygame
import sys
import random

from pygame.locals import *

class Particle(pygame.sprite.Sprite):

    def __init__(self, pos, color):
        super().__init__()

        # random-ing the size from 4 to 10 pixels
        self.SIZE = random.randint(4,10)
        self.color = color

        # using the random size to create random particles
        self.image = pygame.Surface((self.SIZE, self.SIZE))
        self.image.fill(self.color)

        self.rect = self.image.get_rect(center = pos)
        self.pos = pygame.math.Vector2(pos)

        # Random Velocity: Random direction, random speed
        # random.uniform gives float numbers (e.g., -2.5)
        self.velocity = pygame.math.Vector2(random.uniform(-1,1), random.uniform(-1,1))

        # speed for the particle
        self.velocity = self.velocity.normalize() * random.randint(50,200)

        # how many seconds the particle to exist
        self.lifetime = random.uniform(0.2, 0.6)

    def update(self, dt):

        # movement for the particle
        self.pos += self.velocity * dt
        self.rect.center = (int(self.pos.x), int(self.pos.y))

        # reducing the lifetime
        self.lifetime -= dt

        # death check
        if self.lifetime <= 0:

            # remove it
            self.kill()

        if self.SIZE > 0:
            self.SIZE -= 10 * dt

            if self.SIZE < 1:
                self.SIZE = 0

            self.image = pygame.Surface((int(self.SIZE), int(self.SIZE)), pygame.SRCALPHA)
            self.image.fill(self.color)


class Main:
    def __init__(self):

        pygame.init()
        self.DISPLAY_WIDTH = 800
        self.DISPLAY_HEIGHT = 600
        self.DISPLAY = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))

        self.CLOCK = pygame.time.Clock()
        self.FPS = 60

    def run(self):

        particle_group = pygame.sprite.Group()

        while True:

            dt = self.CLOCK.tick(self.FPS) / 1000

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i in range(30):
                        p = Particle(event.pos, (250,50,50))
                        particle_group.add(p)

            mouse_buttons = pygame.mouse.get_pressed()

            if mouse_buttons[2]:
                pos = pygame.mouse.get_pos()

                for i in range(2):
                    p = Particle(pos, (50, 200, 255))
                    particle_group.add(p)

            particle_group.update(dt)

            self.DISPLAY.fill((50,50,50))
            particle_group.draw(self.DISPLAY)

            pygame.display.update()


if __name__ == "__main__":
    app = Main()
    app.run()