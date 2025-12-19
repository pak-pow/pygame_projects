import random
import pygame
import sys

from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 100, 255))

        self.rect = self.image.get_rect(center=(400, 300))
        self.pos = pygame.Vector2(self.rect.center)
        self.velocity = pygame.Vector2()

        self.acceleration = 3000
        self.max_speed = 300
        self.friction = 0.90
        self.threshold = 10

        # RPG STATS
        self.current_hp = 100
        self.max_hp = 100
        self.xp = 0
        self.max_xp = 50
        self.level = 1

    def take_damage(self, amount):
        self.current_hp -= amount
        if self.current_hp < 0:
            self.current_hp = 0

    def gain_xp(self, amount):
        old_level = self.level
        self.xp += amount

        while self.xp >= self.max_xp:
            self.xp -= self.max_xp
            self.level += 1
            self.max_xp = int(self.max_xp * 1.5)
            self.max_hp += 20
            self.current_hp = self.max_hp
            print(f"Level Up! Now Level {self.level}")

        return self.level > old_level

    def update(self, dt):
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(0, 0)

        if keys[K_w]:
            direction.y -= 1
        if keys[K_s]:
            direction.y += 1
        if keys[K_a]:
            direction.x -= 1
        if keys[K_d]:
            direction.x += 1

        if direction.length_squared() > 0:
            direction = direction.normalize()
            self.velocity += direction * self.acceleration * dt
        else:
            self.velocity *= self.friction
            if self.velocity.length() < self.threshold:
                self.velocity.update(0, 0)

        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        self.pos += self.velocity * dt

        self.pos.x = max(20, min(Main.DISPLAY_WIDTH - 20, self.pos.x))
        self.pos.y = max(20, min(Main.DISPLAY_HEIGHT - 20, self.pos.y))

        self.rect.center = self.pos

class Main:

    DISPLAY_WIDTH = 800
    DISPLAY_HEIGHT = 600
    DISPLAY_COLOR = (0,0,0)

    def __init__(self):

        pygame.init()
        self.DISPLAY = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
        pygame.display.set_caption("DAY22")

        self.FONT = pygame.font.SysFont("Arial", 24)
        self.STAT_FONT = pygame.font.SysFont("Arial", 24)

        self.CLOCK = pygame.time.Clock()
        self.FPS = 60

    def run(self):
        all_sprite = pygame.sprite.Group()
        player = Player()

        all_sprite.add(player)

        while True:

            dt = self.CLOCK.tick(self.FPS) / 1000

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            all_sprite.update(dt)
            self.DISPLAY.fill(self.DISPLAY_COLOR)

            hint = self.FONT.render("[SPACE] Damage   [X] Gain XP", True, (150, 150, 150))
            self.DISPLAY.blit(hint, (20, 550))

            all_sprite.draw(self.DISPLAY)

            pygame.display.update()

if __name__ == "__main__":
    app = Main()
    app.run()