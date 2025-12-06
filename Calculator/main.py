# ==========================================
#  CALCULATOR — REFACTORED CLEAN VERSION
# ==========================================

import pygame, sys
from pygame.locals import *

# -------------------------------
# Button Class (Reusable)
# -------------------------------
class Button:
    """
    CHANGE: Added Button class to remove repetitive button definitions
    UNCHANGED: Button properties (position, size, text) stay the same

    Each button stores:
    - text: the label (number or operator)
    - rect: pygame.Rect for the button size & position
    - text_surf: pre-rendered text surface
    - text_rect: text rectangle centered in button
    """

    def __init__(self, text, rect, font, bg_color=(217,217,217), text_color=(0,0,0)):
        self.text = text
        self.rect = pygame.Rect(rect)
        self.bg_color = bg_color

        # Render text once (faster than re-rendering every frame)
        self.text_surf = font.render(text, True, text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, screen):
        """
        CHANGE: Unified button drawing method
        UNCHANGED: Visual appearance (grey rectangle + black text)
        """
        pygame.draw.rect(screen, self.bg_color, self.rect)
        screen.blit(self.text_surf, self.text_rect)

    def clicked(self, mouse_pos):
        """
        CHANGE: Encapsulates click detection
        UNCHANGED: Functionality is equivalent to collidepoint checks in original
        """
        return self.rect.collidepoint(mouse_pos)


# -------------------------------
# Main Program
# -------------------------------
def main():

    # UNCHANGED: Initialize Pygame and font
    pygame.init()
    font = pygame.font.SysFont(None, 40)
    display = pygame.display.set_mode((500, 700))

    # UNCHANGED: Current input displayed in the calculator
    current_input = ""

    # UNCHANGED: Display box for showing the calculation/result
    display_box = pygame.Rect(25, 25, 450, 100)
    grey = (217, 217, 217)

    # -------------------------------
    # BUTTON DEFINITIONS
    # -------------------------------
    # CHANGE: Using list of tuples instead of 40+ repeated Rects
    numbers = [
        ("1", (25,180,80,100)), ("2", (125,180,80,100)), ("3", (225,180,80,100)),
        ("4", (25,300,80,100)), ("5", (125,300,80,100)), ("6", (225,300,80,100)),
        ("7", (25,420,80,100)), ("8", (125,420,80,100)), ("9", (225,420,80,100)),
        ("0", (25,540,80,100)), ("00", (125,540,80,100)), ("000", (225,540,80,100)),
    ]

    ops = [
        ("+", (325,180,60,180)), ("-", (400,180,60,180)),
        ("*", (325,380,60,180)), ("/", (400,380,60,180)),
        ("=", (325,580,135,60)), ("C", (25,133,80,40)),
    ]

    # CHANGE: Create Button objects for numbers and operators
    buttons = [Button(text, rect, font) for text, rect in numbers + ops]

    # -------------------------------
    # Button click handler
    # -------------------------------
    def handle_button(text, current):
        """
        CHANGE: Unified button click handler instead of 40 if statements
        UNCHANGED: Calculator functionality, including symbols, 0/00/000, C, =, and easter egg

        Logic:
        - "C": reset current input
        - "=": evaluate current input (preserves "5+5" easter egg)
        - otherwise: append button text to current input
        """
        if text == "C":
            return ""
        if text == "=":
            if current == "5+5":
                return "Hello world"  # easter egg
            try:
                return str(eval(current))  # evaluate math
            except:
                return "ERROR"
        return current + text


    # -------------------------------
    # GAME LOOP
    # -------------------------------
    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # CHANGE: Loop through all buttons for clicks instead of repeated ifs
                for btn in buttons:
                    if btn.clicked(mouse_pos):
                        current_input = handle_button(btn.text, current_input)

        # ----------------------
        # DRAWING SECTION
        # ----------------------
        display.fill((255,255,255))               # UNCHANGED: White background
        pygame.draw.rect(display, grey, display_box)
        pygame.draw.line(display, grey, (0,150), (500,150))

        # CHANGE: Unified button drawing
        for btn in buttons:
            btn.draw(display)

        # UNCHANGED: Draw current input text inside display box
        display_text = font.render(current_input, True, (0,0,0))
        display.blit(display_text, (display_box.x+20, display_box.y+30))

        pygame.display.update()


if __name__ == "__main__":
    main()
