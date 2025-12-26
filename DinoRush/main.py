import pygame
import sys

from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((30,30))
        self.image.fill((255,0,0))

        self.rect = self.image.get_rect(center = (100, 535))
        self.pos = pygame.Vector2(self.rect.center)
        self.velocity = pygame.Vector2()

        self.on_ground = True
        self.jump_count = 0
        self.max_jump = 1

    def jump(self):

        if self.jump_count < self.max_jump:
            self.velocity.y = Main.JUMP_STRENGTH
            self.jump_count += 1

    def update(self, dt):

        keys = pygame.key.get_pressed()
        self.velocity.x = 0

        self.velocity.y += Main.GRAVITY * dt
        self.pos += self.velocity * dt

        if self.pos.y >= Main.FLOOR_Y:
            self.pos.y = Main.FLOOR_Y

            self.velocity.y = 0
            self.on_ground = True
            self.jump_count = 0

        else:
            self.on_ground = False

        self.rect.midbottom = round(self.pos)

class Main:

    DISPLAY_WIDTH = 1000
    DISPLAY_HEIGHT = 600
    DISPLAY_COLOR = (230,230,230)

    CLOCK = pygame.time.Clock()
    FPS = 60

    GRAVITY = 2000
    JUMP_STRENGTH = - 800
    MOVE_SPEED = 800
    FLOOR_Y = 550

    def __init__(self):

        pygame.init()
        self.DISPLAY = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
        pygame.display.set_caption("DINO RUSH")

    def run(self):

        all_sprites = pygame.sprite.Group()
        player = Player()

        all_sprites.add(player)

        while True:

            dt = self.CLOCK.tick(self.FPS) / 1000

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        player.jump()

            all_sprites.update(dt)
            self.DISPLAY.fill(self.DISPLAY_COLOR)

            all_sprites.draw(self.DISPLAY)
            pygame.draw.line(self.DISPLAY, (0,0,0), (0,550), (1000,550), 2)
            pygame.display.update()

if __name__ == "__main__":
    app = Main()
    app.run()