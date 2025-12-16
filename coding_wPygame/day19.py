import random
import pygame
import sys
from pygame.locals import *


class Wall(pygame.sprite.Sprite):
    def __init__(self, rect):
        super().__init__()
        self.image = pygame.Surface((rect.width, rect.height))
        self.image.fill((80, 80, 80))
        self.rect = rect


# ================= PLAYER =================
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((30, 30))
        self.image.fill((0, 255, 0))

        self.rect = self.image.get_rect(center=(400, 300))
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 250

    def update(self, dt):
        keys = pygame.key.get_pressed()
        direction = pygame.math.Vector2(0, 0)

        if keys[K_w]: direction.y -= 1
        if keys[K_s]: direction.y += 1
        if keys[K_a]: direction.x -= 1
        if keys[K_d]: direction.x += 1

        if direction.length() > 0:
            direction.normalize_ip()
            self.pos += direction * self.speed * dt

        # screen bounds
        self.pos.x = max(15, min(Main.DISPLAY_WIDTH - 15, self.pos.x))
        self.pos.y = max(15, min(Main.DISPLAY_HEIGHT - 15, self.pos.y))

        self.rect.center = (round(self.pos.x), round(self.pos.y))


# ================= ENEMY =================
class Enemy(pygame.sprite.Sprite):
    def __init__(self, player, walls):
        super().__init__()

        self.image = pygame.Surface((30, 30))
        self.image.fill((120, 50, 50))
        self.rect = self.image.get_rect(center=(100, 100))
        self.pos = pygame.math.Vector2(self.rect.center)

        self.player = player
        self.walls = walls

        self.speed = 150
        self.aggro_radius = 200

        self.state = "WANDER"

        self.wander_target = self.random_target()
        self.wander_timer = 0

        # 🧠 MEMORY
        self.last_seen_pos = None
        self.memory_time = 0
        self.memory_duration = 3.0  # seconds

    def random_target(self):
        return pygame.math.Vector2(
            random.randint(30, Main.DISPLAY_WIDTH - 30),
            random.randint(30, Main.DISPLAY_HEIGHT - 30)
        )

    def can_see_player(self):
        start = self.pos
        end = self.player.pos
        ray = end - start

        if ray.length() == 0:
            return False

        ray.normalize_ip()
        step = 5
        current = pygame.math.Vector2(start)

        for _ in range(int((end - start).length() / step)):
            current += ray * step
            for wall in self.walls:
                if wall.rect.collidepoint(current):
                    return False
        return True

    def update(self, dt):
        to_player = self.player.pos - self.pos
        distance = to_player.length()
        sees_player = distance < self.aggro_radius and self.can_see_player()

        # ---------- STATE LOGIC ----------
        if sees_player:
            self.state = "CHASE"
            self.last_seen_pos = self.player.pos.copy()
            self.memory_time = self.memory_duration

        elif self.memory_time > 0:
            self.state = "SEARCH"
            self.memory_time -= dt

        else:
            self.state = "WANDER"

        # ---------- ACTIONS ----------
        if self.state == "CHASE":
            self.image.fill((255, 0, 0))
            if distance > 0:
                self.pos += to_player.normalize() * self.speed * dt

        elif self.state == "SEARCH":
            self.image.fill((0, 120, 255))
            to_memory = self.last_seen_pos - self.pos

            if to_memory.length() > 5:
                self.pos += to_memory.normalize() * self.speed * dt
            else:
                self.memory_time = 0  # reached spot

        else:  # WANDER
            self.image.fill((120, 50, 50))
            self.wander_timer += dt

            if self.wander_timer > 2:
                self.wander_target = self.random_target()
                self.wander_timer = 0

            to_target = self.wander_target - self.pos
            if to_target.length() > 5:
                self.pos += to_target.normalize() * self.speed * 0.5 * dt

        self.rect.center = (round(self.pos.x), round(self.pos.y))

class Main:
    DISPLAY_WIDTH = 800
    DISPLAY_HEIGHT = 600
    DISPLAY_COLOR = (10, 10, 20)

    def __init__(self):

        pygame.init()
        self.DISPLAY = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))

        pygame.display.set_caption("DAY 19 – AI STATES")
        self.CLOCK = pygame.time.Clock()
        self.FPS = 60

    def run(self):
        player = Player()

        walls = pygame.sprite.Group(
            Wall(pygame.Rect(300, 200, 200, 30)),
            Wall(pygame.Rect(150, 400, 300, 30))
        )

        enemy = Enemy(player, walls)
        all_sprites = pygame.sprite.Group(player, enemy, *walls)

        while True:
            dt = self.CLOCK.tick(self.FPS) / 1000

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            if enemy.last_seen_pos:
                pygame.draw.circle(
                    self.DISPLAY,
                    (0, 150, 255),
                    enemy.last_seen_pos,
                    5
                )

            all_sprites.update(dt)

            self.DISPLAY.fill(self.DISPLAY_COLOR)

            # DEBUG visuals
            pygame.draw.circle(
                self.DISPLAY, (60, 60, 60),
                enemy.rect.center, enemy.aggro_radius, 1
            )

            pygame.draw.line(
                self.DISPLAY, (255, 255, 0),
                enemy.rect.center, player.rect.center, 1
            )

            all_sprites.draw(self.DISPLAY)
            pygame.display.flip()


if __name__ == "__main__":
    app = Main()
    app.run()