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
        self.dash_duration = 0.2
        self.dash_time_left = 0
        self.dash_cooldown = 0.5
        self.dash_timer = 0

        # INVENTORY VARIABLES
        self.inventory = []
        self.capacity = 5

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

        if direction.length_squared() > 0:
            direction = direction.normalize()

        # CHECK DASH
        if keys[K_LSHIFT] and not self.is_dashing and self.dash_timer <= 0 and direction.length_squared() > 0:
            self.is_dashing = True
            self.dash_time_left = self.dash_duration
            self.dash_timer = self.dash_cooldown
            self.vel = direction * self.dash_speed

        # MOVEMENT PHYSICS
        if self.is_dashing:
            self.dash_time_left -= dt
            if self.dash_time_left <= 0:
                self.is_dashing = False
                self.vel *= 0.5
        else:
            if direction.length_squared() > 0:
                self.vel += direction * self.acceleration * dt
            else:
                self.vel *= self.friction
                if self.vel.length() < 10:
                    self.vel.update(0, 0)

            if self.vel.length() > self.max_speed:
                self.vel.scale_to_length(self.max_speed)

        self.pos += self.vel * dt

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
        pygame.display.set_caption("DAY21 - Inventory Integrated")
        self.CLOCK = pygame.time.Clock()
        self.FPS = 60

        self.near_item = None
        self.show_inventory = False  # State to toggle inventory UI

        self.font_small = pygame.font.SysFont("Arial", 20)
        self.font_large = pygame.font.SysFont("Arial", 32)

    def draw_mini_popup(self, item, inventory_full):
        item_x = item.rect.centerx
        item_y = item.rect.top - 10

        box_width = 160
        box_height = 70
        box_x = item_x - (box_width // 2)
        box_y = item_y - box_height

        box = pygame.Rect(box_x, box_y, box_width, box_height)

        pygame.draw.rect(self.DISPLAY, (30, 30, 30), box)
        pygame.draw.rect(self.DISPLAY, (255, 255, 255), box, 1)

        # Dynamic Text: Change prompt if inventory is full
        if inventory_full:
            label = self.font_small.render("Bag Full!", True, (255, 50, 50))
            options = self.font_small.render("[N] Leave", True, (200, 200, 200))
        else:
            label = self.font_small.render(f"Pick up {item.name}?", True, (255, 255, 255))
            options = self.font_small.render("[Y] Yes  [N] No", True, (200, 200, 200))

        self.DISPLAY.blit(label, (box.centerx - label.get_width() // 2, box.y + 10))
        self.DISPLAY.blit(options, (box.centerx - options.get_width() // 2, box.y + 35))

        pygame.draw.polygon(self.DISPLAY, (255, 255, 255), [
            (item_x, item_y),
            (item_x - 5, item_y - 5),
            (item_x + 5, item_y - 5)
        ])

    def draw_inventory_screen(self, inventory):
        # 1. Dark Overlay
        overlay = pygame.Surface((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.DISPLAY.blit(overlay, (0, 0))

        # 2. The Panel
        panel_rect = pygame.Rect(200, 100, 400, 400)
        pygame.draw.rect(self.DISPLAY, (40, 40, 40), panel_rect)
        pygame.draw.rect(self.DISPLAY, (255, 255, 255), panel_rect, 2)

        # 3. Title
        title = self.font_large.render("INVENTORY", True, (255, 255, 255))
        self.DISPLAY.blit(title, (panel_rect.centerx - title.get_width() // 2, panel_rect.y + 20))

        # 4. Items List
        y_offset = panel_rect.y + 80
        if not inventory:
            empty_text = self.font_small.render("(Empty)", True, (150, 150, 150))
            self.DISPLAY.blit(empty_text, (panel_rect.centerx - empty_text.get_width() // 2, y_offset))
        else:
            for i, item_name in enumerate(inventory):
                text = self.font_small.render(f"{i + 1}. {item_name}", True, (255, 255, 255))
                self.DISPLAY.blit(text, (panel_rect.x + 40, y_offset))
                y_offset += 40

    def apply_push_back(self, player, item):
        push_vector = player.pos - pygame.Vector2(item.rect.center)
        if push_vector.length() > 0:
            push_vector = push_vector.normalize()
            knockback_strength = 600
            player.vel = push_vector * knockback_strength

    def run(self):
        all_sprite = pygame.sprite.Group()
        item_group = pygame.sprite.Group()
        player = Player()

        all_sprite.add(player)

        # Create Items
        for i in range(3):
            item = Items("Potion", (0, 200, 255))
            item_group.add(item)
            all_sprite.add(item)

        for i in range(2):
            item = Items("Coin", (255, 215, 0))
            item_group.add(item)
            all_sprite.add(item)

        while True:
            dt = self.CLOCK.tick(self.FPS) / 1000

            # 1. FIND NEAREST ITEM (Interaction Check)
            # We check a slightly larger area (inflated by 20 pixels)
            # This keeps the popup open even if we are pushed back a tiny bit.
            interaction_rect = player.rect.inflate(20, 20)
            nearby_hits = []

            # Manual check for nearby items
            for item in item_group:
                if interaction_rect.colliderect(item.rect):
                    nearby_hits.append(item)

            if nearby_hits:
                self.near_item = nearby_hits[0]
            else:
                self.near_item = None

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_i:
                        self.show_inventory = not self.show_inventory

                    # INPUT LOGIC (Uses self.near_item found above)
                    if not self.show_inventory and self.near_item:
                        if event.key == K_y:
                            if len(player.inventory) < player.capacity:
                                print(f"Collected: {self.near_item.name}")
                                player.inventory.append(self.near_item.name)
                                item_group.remove(self.near_item)
                                all_sprite.remove(self.near_item)
                                self.near_item = None
                            else:
                                print("Inventory Full!")

                        elif event.key == K_n:
                            self.apply_push_back(player, self.near_item)

            # --- UPDATE & PHYSICS ---
            if not self.show_inventory:
                all_sprite.update(dt)

                # PHYSICS CHECK (Strict collision)
                # This stops the player from walking INSIDE the item
                # But it won't kill the popup because we used 'interaction_rect' above
                hits = pygame.sprite.spritecollide(player, item_group, False)
                if hits:
                    player.pos = player.prev_pos.copy()
                    player.rect.center = player.pos
                    player.vel.update(0, 0)

            # --- DRAWING ---
            self.DISPLAY.fill(self.DISPLAY_COLOR)
            all_sprite.draw(self.DISPLAY)

            if self.near_item and not self.show_inventory:
                is_full = len(player.inventory) >= player.capacity
                self.draw_mini_popup(self.near_item, is_full)

            if self.show_inventory:
                self.draw_inventory_screen(player.inventory)
            else:
                hint = self.font_small.render("[I] Inventory", True, (200, 200, 200))
                self.DISPLAY.blit(hint, (10, 10))

            pygame.display.update()

if __name__ == "__main__":
    app = Main()
    app.run()