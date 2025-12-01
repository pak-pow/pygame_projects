"""
Day 4 understanding FPS
"""

import pygame, sys
from pygame.time import Clock
from pygame.locals import *

def main():

    pygame.init()
    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 500

    DISPLAY = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

    clock = Clock()
    FPS = 60

    # CHARACTERS
    RED_rect = pygame.Rect(50,100,50,50)
    R_Speed_per_frame = 5

    BLUE_rect = pygame.Rect(50,250,50,50)
    B_Speed_per_second = 300
    B_pos_x = 50.0

    # GAME LOOP
    running = True
    while running:

        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    RED_rect.x = 50
                    BLUE_rect.x = 50
                    B_pos_x = 50.0

        RED_rect.x += R_Speed_per_frame

        B_pos_x += B_Speed_per_second * dt
        BLUE_rect.x = int(B_pos_x)  # Update rect (must be int)

        # Boundary Wrap (Loop around screen)
        if RED_rect.left > 600: RED_rect.right = 0
        if BLUE_rect.left > 600: B_pos_x = -50

        DISPLAY.fill((255,255,255))

        pygame.draw.rect(DISPLAY, (255, 0, 0), RED_rect) # Red
        pygame.draw.rect(DISPLAY, (0, 0, 255), BLUE_rect) # Blue

        # Display FPS in caption
        pygame.display.set_caption(f"FPS: {int(clock.get_fps())} | DT: {dt:.4f}")
        pygame.display.update()

    pass

if __name__ == "__main__":
    main()