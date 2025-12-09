import pygame
import sys
import random

from pygame.locals import *

class Particle(pygame.sprite.Sprite):

    def __init__(self, pos, color):
        super().__init__()

        self.SIZE = random.randint(4, 10)

        self.target_color = color
        self.current_color = (255, 255, 255)

        self.image = pygame.Surface((self.SIZE, self.SIZE))
        self.image.fill(self.current_color)

        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)

        self.velocity = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))

        if self.velocity.length() == 0:
            self.velocity = pygame.math.Vector2(0, -1)

        self.velocity = self.velocity.normalize() * random.randint(50, 200)

        self.lifetime = random.uniform(0.2, 0.6)
        self.start_lifetime = self.lifetime  # Remember original life for the math

    def update(self, dt):
        self.pos += self.velocity * dt
        self.rect.center = (int(self.pos.x), int(self.pos.y))

        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()

        life_ratio = self.lifetime / self.start_lifetime

        life_ratio = max(0, min(1, life_ratio))
        r = int(self.target_color[0] + (255 - self.target_color[0]) * life_ratio)
        g = int(self.target_color[1] + (255 - self.target_color[1]) * life_ratio)
        b = int(self.target_color[2] + (255 - self.target_color[2]) * life_ratio)

        self.current_color = (r, g, b)

        if self.SIZE > 0:
            self.SIZE -= 10 * dt

            if self.SIZE < 1:
                self.SIZE = 0

            self.image = pygame.Surface((int(self.SIZE), int(self.SIZE)), pygame.SRCALPHA)
            self.image.fill(self.current_color)

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
                        p = Particle(event.pos, (250, 50, 50))
                        particle_group.add(p)

            mouse_buttons = pygame.mouse.get_pressed()
            if mouse_buttons[2]:
                pos = pygame.mouse.get_pos()
                for i in range(2):
                    p = Particle(pos, (50, 200, 255))
                    particle_group.add(p)

            particle_group.update(dt)

            self.DISPLAY.fill((50, 50, 50))
            particle_group.draw(self.DISPLAY)

            pygame.display.update()


if __name__ == "__main__":
    app = Main()
    app.run()