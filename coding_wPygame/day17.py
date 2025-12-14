import os.path
import pygame
import sys
import json

from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

    def input_check(self):
        pass

    def update(self, dt):
        pass

class Main:

    DISPLAY_WIDTH = 800
    DISPLAY_HEIGHT = 600
    DISPLAY_COLOR = (255,255,255)

    def __init__(self):

        pygame.init()
        pygame.display.set_caption("DAY17 FILE I/O")
        self.DISPLAY = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))

        self.CLOCK = pygame.time.Clock()
        self.FPS = 60

        # =================
        self.SAVE_FILE = "game_data.json"
        # =================

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
                "coin": 0
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

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.DISPLAY.fill(self.DISPLAY_COLOR)
            pygame.display.update()

if __name__ == "__main__":
    app = Main()
    app.run()