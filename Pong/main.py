""""
PONG GAME — TO-DO LIST
----------------------

TODO:
    📌 STAGE 1 — BASE SETUP
        - Create the main game window (size, caption, FPS) [DONE]
        - Initialize Pygame, Clock(), and delta time (dt) [DONE]
        - Create the game loop structure (running = True) [DONE]
        - Clear screen + update display every frame [DONE]

    📌 STAGE 2 — OBJECT CREATION
        - Create paddle rectangles (left & right) [DONE]
        - Create ball rectangle [DONE]
        - Add variables for paddle speed (px/s) [DONE]
        - Add variables for ball speed (px/s) + direction vector [DONE]

    📌 STAGE 3 — PADDLE MOVEMENT
        - Implement player controls for left paddle (W/S or ↑/↓) [DONE]
        - Make paddle movement use delta time (time-based) [DONE]
        - Prevent paddles from leaving screen boundaries [DONE]

    📌 STAGE 4 — BALL PHYSICS
        - Move the ball using dt (ball_pos_x, ball_pos_y as floats) [DONE]
        - Detect collision with top and bottom walls → bounce [DONE]
        - Detect collision with paddles → bounce horizontally [DONE]
        - Add ball speed increase after each paddle hit (optional)

    📌 STAGE 5 — SCORING SYSTEM
        - Detect when ball exits the screen [DONE]
        - Add score counters for Player 1 and Player 2
        - Reset ball to center when a point is scored
        - Serve the ball toward the player who was scored on

    📌 STAGE 6 — GAME POLISH
        - Add center dividing line
        - Add text rendering for scores
        - Add game restart on SPACE
        - Add simple sound effects (bounce, score) (optional)

    📌 STAGE 7 — EXTRA FEATURES (Optional)
        - Add difficulty settings (ball speed, paddle speed)
        - Add AI/bot for Player 2 (easy/medium/hard)
        - Add smooth paddle acceleration instead of instant movement
        - Add color themes (classic, neon, dark mode)
        - Add FPS + dt display for debugging
        - Add main menu screen
"""""

# ================================= MAIN CODE ===================================

# importing libraries
import pygame
import sys
import pygame.font
import random

from pygame.locals import *
from pygame.time import Clock

def main():

    # initialize the pygame
    pygame.init()

    # font
    font = pygame.font.SysFont(None, 32)

    # display
    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 700
    DISPLAY = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

    # clock
    clock = Clock()
    FPS = 60

    # player object
    PLAYER_OBJ = pygame.Rect(200,600,200,25)
    PLAYER_speed_per_second = 500
    PLAYER_pos_x = float(PLAYER_OBJ.x)

    # Ball object
    ball_started = False
    BALL_OBJ = pygame.Rect(200,100,30,30)

    BALL_SPEED_X = 0.0
    BALL_SPEED_Y = 500.0

    BALL_POS_X = float(BALL_OBJ.x)
    BALL_POS_Y = float(BALL_OBJ.y)

    # color
    PLAYER_COLOR = (0,0,0)
    BALL_COLOR = (0,0,0)

    # movements
    M_left = False
    M_right = False

    # game loop
    while True:

        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():

            # check for quit
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # down
            if event.type == KEYDOWN:

                if event.key == K_LEFT or event.key == K_a:
                    M_left = True

                if event.key == K_RIGHT or event.key == K_d:
                    M_right = True

            # up
            if event.type == KEYUP:

                if event.key == K_LEFT or event.key == K_a:
                    M_left = False

                if event.key == K_RIGHT or event.key == K_d:
                    M_right = False


        # movement logic
        if M_left:
            PLAYER_pos_x -= PLAYER_speed_per_second * dt
            PLAYER_OBJ.x = int(PLAYER_pos_x)

        if M_right:
            PLAYER_pos_x += PLAYER_speed_per_second * dt
            PLAYER_OBJ.x = int(PLAYER_pos_x)

        if PLAYER_OBJ.left < 0:
            PLAYER_OBJ.left = 0
            PLAYER_pos_x = float(PLAYER_OBJ.x)

        if PLAYER_OBJ.right > 600:
            PLAYER_OBJ.right = 600
            PLAYER_pos_x = float(PLAYER_OBJ.x)

        # dropping ball logic & Update position using delta time
        BALL_POS_X += BALL_SPEED_X * dt
        BALL_POS_Y += BALL_SPEED_Y * dt

        # Update the rect
        BALL_OBJ.x = int(BALL_POS_X)
        BALL_OBJ.y = int(BALL_POS_Y)

        if BALL_OBJ.top <= 0:

            BALL_SPEED_Y *= -1
            BALL_OBJ.top = 0

            BALL_POS_Y = float(BALL_OBJ.y)

        if BALL_OBJ.left <= 0:

            BALL_OBJ.left = 0
            BALL_SPEED_X *= -1

        elif BALL_OBJ.right >= WINDOW_WIDTH:

            BALL_OBJ.right = WINDOW_WIDTH
            BALL_SPEED_X *= -1

            # Update float after snapping
        BALL_POS_X = float(BALL_OBJ.x)

        # Collision detection
        if BALL_OBJ.colliderect(PLAYER_OBJ):
            BALL_SPEED_Y *= -1
            BALL_OBJ.bottom = PLAYER_OBJ.top
            BALL_POS_Y = float(BALL_OBJ.y)

            # Calculate offset (center of ball vs center of paddle)
            offset = (BALL_OBJ.centerx - PLAYER_OBJ.centerx)

            # Add that offset to the X speed (steer the ball!)
            BALL_SPEED_X += offset * 5

            if not ball_started:
                BALL_SPEED_X = random.choice([-200.0,-150.0,150.0,200.0])
                ball_started = True


        # --- BALL FALLS BELOW SCREEN (RESET) ---
        if BALL_OBJ.bottom >= WINDOW_HEIGHT:

            # RESET everything
            BALL_OBJ.x = WINDOW_WIDTH // 2
            BALL_OBJ.y = 100

            BALL_POS_X = float(BALL_OBJ.x)
            BALL_POS_Y = float(BALL_OBJ.y)

            BALL_SPEED_X = 0       # straight down again
            BALL_SPEED_Y = 400.0
            ball_started = False


        # RENDER
        DISPLAY.fill((255,255,255))

        # Rendering FPS
        text_surface = font.render(f"FPS: {int(clock.get_fps())}", True, (0, 0, 0))
        DISPLAY.blit(text_surface, (10,10))

        # Rendering the player and the ball
        pygame.draw.rect(DISPLAY,PLAYER_COLOR, PLAYER_OBJ)
        pygame.draw.rect(DISPLAY,BALL_COLOR, BALL_OBJ)

        # updating the pygame
        pygame.display.update()



if __name__ == "__main__":
    main()