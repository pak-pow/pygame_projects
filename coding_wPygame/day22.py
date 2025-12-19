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


class Trap(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()

        self.rect.x = random.randint(50, Main.DISPLAY_WIDTH - 50)
        self.rect.y = random.randint(50, Main.DISPLAY_HEIGHT - 50)

        self.damage = 15


class Main:
    DISPLAY_WIDTH = 800
    DISPLAY_HEIGHT = 600
    DISPLAY_COLOR = (30, 30, 30)

    def __init__(self):
        pygame.init()
        self.DISPLAY = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
        pygame.display.set_caption("DAY 22 - Health Ui Bar")

        self.FONT = pygame.font.SysFont("Arial", 24)
        self.STAT_FONT = pygame.font.SysFont("Arial", 16, bold=True)

        self.CLOCK = pygame.time.Clock()
        self.FPS = 60

    def draw_interface(self, player):
        bar_x, bar_y = 20, 20
        bar_w, bar_h = 200, 25

        if player.max_hp > 0:
            ratio = player.current_hp / player.max_hp
        else:
            ratio = 0

        fill_w = bar_w * ratio

        # Red Background
        pygame.draw.rect(self.DISPLAY, (100, 0, 0), (bar_x, bar_y, bar_w, bar_h))
        # Green Foreground
        pygame.draw.rect(self.DISPLAY, (0, 200, 50), (bar_x, bar_y, fill_w, bar_h))
        # White Border
        pygame.draw.rect(self.DISPLAY, (255, 255, 255), (bar_x, bar_y, bar_w, bar_h), 2)

        hp_text = self.STAT_FONT.render(
            f"{player.current_hp}/{player.max_hp}", True, (255, 255, 255)
        )
        self.DISPLAY.blit(hp_text, (bar_x + 70, bar_y + 4))

        xp_text = self.FONT.render(
            f"LVL: {player.level}   XP: {player.xp}/{player.max_xp}",
            True, (255, 255, 255)
        )
        self.DISPLAY.blit(xp_text, (20, 60))

        # Display if player is dead
        if player.current_hp <= 0:
            dead_text = self.FONT.render("DEAD - Press R to restart", True, (255, 0, 0))
            self.DISPLAY.blit(dead_text, (250, 280))

    def restart_game(self):
        return Player()

    def run(self):
        all_sprite = pygame.sprite.Group()
        trap_group = pygame.sprite.Group()

        player = Player()
        all_sprite.add(player)

        for i in range(10):
            trap = Trap()
            trap_group.add(trap)
            all_sprite.add(trap)

        game_over = False

        while True:
            dt = self.CLOCK.tick(self.FPS) / 1000

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        if not game_over:
                            player.take_damage(15)
                    if event.key == K_x:
                        if not game_over:
                            player.gain_xp(20)
                    if event.key == K_r and game_over:
                        player = self.restart_game()
                        all_sprite.empty()
                        trap_group.empty()
                        all_sprite.add(player)
                        for i in range(10):
                            trap = Trap()
                            trap_group.add(trap)
                            all_sprite.add(trap)
                        game_over = False

            if not game_over:
                all_sprite.update(dt)

                trap_collide = pygame.sprite.spritecollide(player, trap_group, True)
                for trap in trap_collide:
                    player.take_damage(trap.damage)
                    print("Player hit Trap")

                if player.current_hp <= 0:
                    game_over = True

            self.DISPLAY.fill(self.DISPLAY_COLOR)
            all_sprite.draw(self.DISPLAY)

            self.draw_interface(player)

            hint = self.FONT.render("[SPACE] Damage   [X] Gain XP   WASD Move   R Restart", True, (150, 150, 150))
            self.DISPLAY.blit(hint, (10, 550))

            pygame.display.update()


if __name__ == "__main__":
    app = Main()
    app.run()