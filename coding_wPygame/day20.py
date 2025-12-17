import pygame, sys, os


# 1. THE ASSET HELPER (CRITICAL FOR EXE)
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# 2. Standard Setup
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("My First Exe")
clock = pygame.time.Clock()

# 3. Load Assets using the Helper
# (Make sure you actually have an icon.png, or remove these lines!)
# icon = pygame.image.load(resource_path("icon.png"))
# pygame.display.set_icon(icon)

font = pygame.font.SysFont("Arial", 40)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((50, 100, 200))

    # Draw instructions
    text = font.render("I AM AN EXE FILE!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(300, 200))
    screen.blit(text, text_rect)

    pygame.display.update()
    clock.tick(60)