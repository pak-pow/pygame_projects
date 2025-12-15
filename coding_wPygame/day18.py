import pygame, sys, random

# 1. Setup
pygame.init()
SCREEN_W, SCREEN_H = 800, 600
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()

# Generate a cool background pattern
bg_surf = pygame.Surface((SCREEN_W, SCREEN_H))
bg_surf.fill((50, 50, 50))
for x in range(0, SCREEN_W, 40):
    pygame.draw.line(bg_surf, (100, 100, 100), (x, 0), (x, SCREEN_H))
for y in range(0, SCREEN_H, 40):
    pygame.draw.line(bg_surf, (100, 100, 100), (0, y), (SCREEN_W, y))

# Draw some random colored boxes to see the lighting better
for i in range(20):
    color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    rect = (random.randint(0, 700), random.randint(0, 500), 50, 50)
    pygame.draw.rect(bg_surf, color, rect)

# --- LIGHTING SETUP ---
# This is the "Filter" layer
light_mask = pygame.Surface((SCREEN_W, SCREEN_H))


# Load or Create a Light Texture (Soft Circle)
# In a real game, you'd load a 'gradient_circle.png'
# Here, we make one manually with circles
def draw_gradient_circle(surf, pos, radius, color):
    # Draw multiple circles with decreasing alpha to simulate softness
    # Note: For true smooth lighting, loading a PNG image is WAY faster
    pygame.draw.circle(surf, color, pos, radius)


mode_cyberpunk = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mode_cyberpunk = not mode_cyberpunk

    # 1. DRAW GAME WORLD (Normal)
    screen.blit(bg_surf, (0, 0))

    mouse_pos = pygame.mouse.get_pos()

    # 2. LIGHTING LOGIC
    if not mode_cyberpunk:
        # --- MODE A: FLASHLIGHT (Multiply) ---

        # A. Fill mask with Darkness (Ambient Light)
        # (30, 30, 30) = Very Dark. (0,0,0) = Pitch Black.
        light_mask.fill((30, 30, 30))

        # B. Cut a hole (Draw White Light)
        # White (255, 255, 255) means "Show 100% of the game color"
        pygame.draw.circle(light_mask, (255, 255, 255), mouse_pos, 100)

        # C. Apply the Mask using MULTIPLY
        # Game * Mask = Final Result
        screen.blit(light_mask, (0, 0), special_flags=pygame.BLEND_MULT)

        txt = "Mode: FLASHLIGHT (Multiply). Click to switch."

    else:
        # --- MODE B: NEON GLOW (Add) ---

        # A. We don't fill with darkness here. We just darken the screen manually first
        # creating a 'night' feel
        night_overlay = pygame.Surface((SCREEN_W, SCREEN_H))
        night_overlay.fill((0, 0, 0))
        night_overlay.set_alpha(200)  # Darken everything
        screen.blit(night_overlay, (0, 0))

        # B. Draw Colored Lights using ADD
        # Create a temp surface for the light
        glow_surf = pygame.Surface((SCREEN_W, SCREEN_H))
        glow_surf.fill((0, 0, 0))  # Black adds nothing

        # Draw Red Light
        pygame.draw.circle(glow_surf, (255, 0, 0), mouse_pos, 80)
        # Draw Blue Light (Offset)
        pygame.draw.circle(glow_surf, (0, 0, 255), (mouse_pos[0] + 50, mouse_pos[1] + 50), 60)

        # C. Apply using ADD
        screen.blit(glow_surf, (0, 0), special_flags=pygame.BLEND_ADD)

        txt = "Mode: CYBERPUNK (Add). Click to switch."

    # UI
    font = pygame.font.SysFont(None, 30)
    screen.blit(font.render(txt, True, (255, 255, 255)), (10, 10))

    pygame.display.update()
    clock.tick(60)