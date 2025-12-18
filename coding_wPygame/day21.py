import random
import pygame
import sys
from pygame.locals import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 255, 0))

        self.rect = self.image.get_rect(center=(400, 300))
        self.pos = pygame.Vector2(self.rect.center)
        self.vel = pygame.Vector2()
        self.prev_pos = self.pos.copy()

        self.acceleration = 3000
        self.max_speed = 300
        self.friction = 0.90

        # DASH VARIABLES
        self.is_dashing = False
        self.dash_speed = 800
        self.dash_duration = 0.2  # FIX 1: Added duration (0.2 seconds is snappy)
        self.dash_time_left = 0
        self.dash_cooldown = 0.5
        self.dash_timer = 0

    def update(self, dt):
        self.prev_pos = self.pos.copy()

        # Reduce cooldown timer
        self.dash_timer = max(0, self.dash_timer - dt)

        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(0, 0)

        if keys[K_w]: direction.y -= 1
        if keys[K_s]: direction.y += 1
        if keys[K_a]: direction.x -= 1
        if keys[K_d]: direction.x += 1

        # NORMALIZE INPUT
        if direction.length_squared() > 0:
            direction = direction.normalize()

        # CHECK DASH TRIGGER
        if keys[K_LSHIFT] and not self.is_dashing and self.dash_timer <= 0 and direction.length_squared() > 0:
            self.is_dashing = True
            self.dash_time_left = self.dash_duration
            self.dash_timer = self.dash_cooldown

            # Apply dash velocity immediately
            self.vel = direction * self.dash_speed

        # --- MOVEMENT LOGIC ---

        if self.is_dashing:
            # FIX 2: While dashing, we count down the timer
            self.dash_time_left -= dt

            # If dash ends, stop dashing and cut velocity slightly
            if self.dash_time_left <= 0:
                self.is_dashing = False
                self.vel *= 0.5  # Optional: slows you down a bit after dash ends

        else:
            # FIX 3: Only apply Normal Acceleration and Speed Limit when NOT dashing
            if direction.length_squared() > 0:
                self.vel += direction * self.acceleration * dt
            else:
                self.vel *= self.friction
                if self.vel.length() < 10:
                    self.vel.update(0, 0)

            # Only limit speed if we are NOT dashing
            if self.vel.length() > self.max_speed:
                self.vel.scale_to_length(self.max_speed)

        # APPLY POSITION
        self.pos += self.vel * dt

        # CLAMP TO SCREEN
        self.pos.x = max(20, min(Main.DISPLAY_WIDTH - 20, self.pos.x))
        self.pos.y = max(20, min(Main.DISPLAY_HEIGHT - 20, self.pos.y))

        self.rect.center = self.pos

class Items(pygame.sprite.Sprite):
    def __init__(self, name, color):
        super().__init__()
        self.name = name
        self.image = pygame.Surface((20, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, Main.DISPLAY_WIDTH - 50)
        self.rect.y = random.randint(50, Main.DISPLAY_HEIGHT - 50)


class Main:

    DISPLAY_WIDTH = 800
    DISPLAY_HEIGHT = 600
    DISPLAY_COLOR = (0, 0, 0)

    def __init__(self):

        pygame.init()
        self.DISPLAY = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))

        pygame.display.set_caption("DAY21")
        self.CLOCK = pygame.time.Clock()
        self.FPS = 60

        self.state = "GAME"
        self.collided_item = None

        # Smaller font for the small popup
        self.font_small = pygame.font.SysFont(None, 24)

    def draw_mini_popup(self):
        if not self.collided_item:
            return

        # 1. Get position relative to the item (Above the item)
        item_x = self.collided_item.rect.centerx
        item_y = self.collided_item.rect.top - 10  # 10 pixels above item

        # 2. Define box size
        box_width = 140
        box_height = 60

        # Center the box horizontally on the item
        box_x = item_x - (box_width // 2)
        box_y = item_y - box_height

        # Create Rect
        box = pygame.Rect(box_x, box_y, box_width, box_height)

        # Draw Box Background and Border
        pygame.draw.rect(self.DISPLAY, (30, 30, 30), box)  # Dark Grey fill
        pygame.draw.rect(self.DISPLAY, (255, 255, 255), box, 1)  # White border

        # Draw Text
        label = self.font_small.render("Collect?", True, (255, 255, 255))
        options = self.font_small.render("[Y] Yes  [N] No", True, (200, 200, 200))

        # Blit text centered in the small box
        self.DISPLAY.blit(label, (box.centerx - label.get_width() // 2, box.y + 5))
        self.DISPLAY.blit(options, (box.centerx - options.get_width() // 2, box.y + 30))

        # Draw a little triangle pointing down to the item (Optional, but looks cool)
        pygame.draw.polygon(self.DISPLAY, (255, 255, 255), [
            (item_x, item_y),
            (item_x - 5, item_y - 5),
            (item_x + 5, item_y - 5)
        ])

    def apply_push_back(self, player):
        # Calculate direction from Item -> Player
        # (This vector points AWAY from the item)
        push_vector = player.pos - pygame.Vector2(self.collided_item.rect.center)

        if push_vector.length() > 0:
            push_vector = push_vector.normalize()

            # Apply force (Knockback strength)
            knockback_strength = 600
            player.vel = push_vector * knockback_strength

    def run(self):
        all_sprite = pygame.sprite.Group()
        item_group = pygame.sprite.Group()
        player = Player()

        all_sprite.add(player)

        for i in range(3):
            item = Items("Potion", (0, 200, 255))
            item_group.add(item)
            all_sprite.add(item)

        while True:
            dt = self.CLOCK.tick(self.FPS) / 1000

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if self.state == "COLLECT_CONFIRM":
                    if event.type == KEYDOWN:

                        if event.key == K_y:
                            item_group.remove(self.collided_item)
                            all_sprite.remove(self.collided_item)
                            self.collided_item = None
                            self.state = "GAME"

                        if event.key == K_n:
                            # 1. Apply the push back
                            self.apply_push_back(player)

                            # 2. Clear item and resume game
                            self.collided_item = None
                            self.state = "GAME"

            # Update Logic
            if self.state == "GAME":
                all_sprite.update(dt)

                collide = pygame.sprite.spritecollide(player, item_group, False)
                if collide:
                    self.state = "COLLECT_CONFIRM"
                    self.collided_item = collide[0]

                    # Stop player immediately so they don't slide through while reading
                    player.pos = player.prev_pos.copy()
                    player.rect.center = player.pos
                    player.vel.update(0, 0)

            # Draw
            self.DISPLAY.fill(self.DISPLAY_COLOR)
            all_sprite.draw(self.DISPLAY)

            if self.state == "COLLECT_CONFIRM":
                # We draw the player and items FIRST (above),
                # then we draw the popup on top of them.
                self.draw_mini_popup()

            pygame.display.update()


if __name__ == "__main__":
    app = Main()
    app.run()