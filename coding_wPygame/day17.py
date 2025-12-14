import os.path
import pygame
import sys
import json

from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((40,40))
        self.image.fill((0,255,0))
        self.rect = self.image.get_rect(center=(400,300))
        self.pos = pygame.Vector2(0,0)

        self.speed = 300

    def input_check(self):

        keys = pygame.key.get_pressed()

        self.pos.x = 0
        self.pos.y = 0

        if keys[K_a]:
            self.pos.x = -1

        if keys[K_d]:
            self.pos.x = 1

        if keys[K_w]:
            self.pos.y = -1

        if keys[K_s]:
            self.pos.y = 1

    def update(self, dt):
        self.input_check()

        if self.pos.length() > 0:
            self.pos = self.pos.normalize()

        self.rect.center += self.pos * self.speed * dt

        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(800, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(600, self.rect.bottom)

class Main:

    DISPLAY_WIDTH = 800
    DISPLAY_HEIGHT = 600
    DISPLAY_COLOR = (255,255,255)

    def __init__(self):

        pygame.init()
        pygame.display.set_caption("DAY17 FILE I/O")
        self.DISPLAY = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
        self.font = pygame.font.SysFont(None, 36)

        self.CLOCK = pygame.time.Clock()
        self.FPS = 60

        # =================
        self.SAVE_FILE = "game_data.json"
        # =================

        self.game_data = self.load_game()

        self.all_sprites = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)

    def load_game(self):

        if not os.path.exists(self.SAVE_FILE):
            print("No Save File found. Creating New one.")
            return {
                "high_score": 0,
                "coins": 0
            }

        try:

            with open(self.SAVE_FILE, "r") as f:
                data = json.load(f)
                print("Loaded:", data)
                return data

        except :
            print("Save File is Corrupted. Starting Fresh.")
            return {
                "high_score": 0,
                "coins": 0
            }

    def save_game(self, data):

        try:
            with open(self.SAVE_FILE, "w") as f:
                json.dump(data, f)
                print("Game Saved!")
        except:
            print("Error saving game.")

    def run(self):

        while True:

            dt = self.CLOCK.tick(self.FPS) / 1000

            for event in pygame.event.get():

                if event.type == QUIT:
                    self.save_game(self.game_data)
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_c:
                        self.game_data["coins"] += 1
                        print("Coins:", self.game_data["coins"])


            self.DISPLAY.fill(self.DISPLAY_COLOR)

            coin_text = self.font.render(
                f"Coins: {self.game_data['coins']}", True, (0, 0, 0)
            )
            self.DISPLAY.blit(coin_text, (10, 10))

            self.all_sprites.update(dt)
            self.all_sprites.draw(self.DISPLAY)
            pygame.display.update()

if __name__ == "__main__":
    app = Main()
    app.run()