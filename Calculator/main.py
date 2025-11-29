# importing important modules
# Such as the Game Module [Pygame] and SYS
import pygame, sys
import pygame.font
from pygame.locals import *

# Defining the main function
# To fully re-learn the classes in python
def main():

    # initializing all imported pygame modules
    # (Essential starting steps for any pygame projects)
    pygame.init()

    # Creating a font object
    # None uses the default system
    # Size being 40
    font = pygame.font.SysFont(None, 40)

    # Creating a window or a display to put all the things we need to do
    # width 500 and height 700 (x, y)
    display = pygame.display.set_mode((500,700))

    # Adding a variable called current input
    # Example "5+5"
    current_input = ""

    # making the display result screen and more or less like the seeing the number
    # Create a rectangle area for the display screen at (x=25, y=25)
    display_result = pygame.Rect(25,25,450,100)

    # Define a color variable (Grey) using RGB values
    display_result_color = (217, 217, 217)

    """ BUTTON DEFINITIONS """
    # pygame.Rect arguments are (x_position, y_position, width, height)

    # Row 1: 1, 2, 3
    button1 = pygame.Rect(25,180,80,100)
    button2 = pygame.Rect(125,180,80,100)
    button3 = pygame.Rect(225,180,80,100)

    # Row 2: 4, 5, 6
    button4 = pygame.Rect(25,300,80,100)
    button5 = pygame.Rect(125,300,80,100)
    button6 = pygame.Rect(225,300,80,100)

    # Row 3: 7, 8, 9
    button7 = pygame.Rect(25,420,80,100)
    button8 = pygame.Rect(125,420,80,100)
    button9 = pygame.Rect(225,420,80,100)

    # Row 4: 0, 00, 000
    button0 = pygame.Rect(25,540,80,100)
    button00 = pygame.Rect(125,540,80,100)
    button000 = pygame.Rect(225,540,80,100)

    # Operations Column (+, -, *, /)
    button_plus = pygame.Rect(325,180,60,180)
    button_minus = pygame.Rect(400,180,60,180)
    button_times = pygame.Rect(325,380,60,180)
    button_divide = pygame.Rect(400,380,60,180)
    button_equals = pygame.Rect(325,580,135,60)

    # Clear button (top left small button)
    button_clear = pygame.Rect(25, 133, 80, 40)

    """ TEXT RENDERING SETUP """
    # We have to "draw" the text into an image (Surface) before we can show it.

    # Step 1: Render the text "1" in black (0,0,0).
    text_surface1 = font.render("1", True, (0,0,0))

    # Step 2: Get the rectangle of that text and center it inside button1.
    text_rect1 = text_surface1.get_rect(center = button1.center)

    # (Repeating this process for all numbers 2-9...)
    text_surface2 = font.render("2", True, (0,0,0))
    text_rect2 = text_surface2.get_rect(center = button2.center)

    text_surface3 = font.render("3", True, (0, 0, 0))
    text_rect3 = text_surface3.get_rect(center=button3.center)

    text_surface4 = font.render("4", True, (0, 0, 0))
    text_rect4 = text_surface4.get_rect(center=button4.center)

    text_surface5 = font.render("5", True, (0, 0, 0))
    text_rect5 = text_surface5.get_rect(center=button5.center)

    text_surface6 = font.render("6", True, (0, 0, 0))
    text_rect6 = text_surface6.get_rect(center=button6.center)

    text_surface7 = font.render("7", True, (0, 0, 0))
    text_rect7 = text_surface7.get_rect(center=button7.center)

    text_surface8 = font.render("8", True, (0, 0, 0))
    text_rect8 = text_surface8.get_rect(center=button8.center)

    text_surface9 = font.render("9", True, (0, 0, 0))
    text_rect9 = text_surface9.get_rect(center=button9.center)

    # (Repeating process for Zeros...)
    text_surface0 = font.render("0", True, (0, 0, 0))
    text_rect0 = text_surface0.get_rect(center=button0.center)

    text_surface00 = font.render("00", True, (0, 0, 0))
    text_rect00 = text_surface00.get_rect(center=button00.center)

    text_surface000 = font.render("000", True, (0, 0, 0))
    text_rect000 = text_surface000.get_rect(center=button000.center)

    # (Repeating process for Symbols...)
    text_surface_plus = font.render("+", True, (0, 0, 0))
    text_rect_plus = text_surface_plus.get_rect(center=button_plus.center)

    text_surface_minus = font.render("-", True, (0, 0, 0))
    text_rect_minus = text_surface_minus.get_rect(center=button_minus.center)

    text_surface_times = font.render("*", True, (0, 0, 0))
    text_rect_times = text_surface_times.get_rect(center=button_times.center)

    text_surface_divide = font.render("/", True, (0, 0, 0))
    text_rect_divide = text_surface_divide.get_rect(center=button_divide.center)

    text_surface_equals = font.render("=", True, (0, 0, 0))
    text_rect_equals = text_surface_equals.get_rect(center=button_equals.center)

    text_surface_clear = font.render("C", True, (0, 0, 0))
    text_rect_clear = text_surface_clear.get_rect(center=button_clear.center)

    """ GAME LOOP """
    # This while loop runs continuously until the user closes the window.
    while True:

        # Check every event (mouse clicks, key presses) that happened since last frame
        for event in pygame.event.get():

            # If the user clicked the 'X' button on the window
            if event.type == QUIT:

                # Shut down pygame
                pygame.quit()

                # Shut down the python script
                sys.exit()

            """ INPUT HANDLING """
            # 'collidepoint(event.pos)' checks if the mouse click happened inside the button
            if event.type == MOUSEBUTTONDOWN and button_clear.collidepoint(event.pos):

                # Reset string to empty
                current_input = ""

            # If button 1 is clicked, add "1" to the current equation string
            if event.type == MOUSEBUTTONDOWN and button1.collidepoint(event.pos):
                current_input += "1"

            if event.type == MOUSEBUTTONDOWN and button2.collidepoint(event.pos):
                current_input += "2"

            if event.type == MOUSEBUTTONDOWN and button3.collidepoint(event.pos):
                current_input += "3"

            if event.type == MOUSEBUTTONDOWN and button4.collidepoint(event.pos):
                current_input += "4"

            if event.type == MOUSEBUTTONDOWN and button5.collidepoint(event.pos):
                current_input += "5"

            if event.type == MOUSEBUTTONDOWN and button6.collidepoint(event.pos):
                current_input += "6"

            if event.type == MOUSEBUTTONDOWN and button7.collidepoint(event.pos):
                current_input += "7"

            if event.type == MOUSEBUTTONDOWN and button8.collidepoint(event.pos):
                current_input += "8"

            if event.type == MOUSEBUTTONDOWN and button9.collidepoint(event.pos):
                current_input += "9"

            if event.type == MOUSEBUTTONDOWN and button0.collidepoint(event.pos):
                current_input += "0"

            if event.type == MOUSEBUTTONDOWN and button00.collidepoint(event.pos):
                current_input += "00"

            if event.type == MOUSEBUTTONDOWN and button000.collidepoint(event.pos):
                current_input += "000"

            # Adding symbols to the equation string
            if event.type == MOUSEBUTTONDOWN and button_plus.collidepoint(event.pos):
                current_input += "+"

            if event.type == MOUSEBUTTONDOWN and button_minus.collidepoint(event.pos):
                current_input += "-"

            if event.type == MOUSEBUTTONDOWN and button_times.collidepoint(event.pos):
                current_input += "*"

            if event.type == MOUSEBUTTONDOWN and button_divide.collidepoint(event.pos):
                current_input += "/"

            # --- CALCULATION LOGIC ---
            if event.type == MOUSEBUTTONDOWN and button_equals.collidepoint(event.pos):

                # added a small easter egg hehe
                if current_input == "5+5":
                    current_input = "Hello world"

                else:
                    try:
                        # eval() takes a string like "5+5" and does the math (returns 10)
                        # We wrap it in str() to turn the number 10 back into text "10"
                        current_input = str(eval(current_input))

                    except:

                        # If the math is impossible (like dividing by zero), show ERROR
                        current_input = "ERROR"


        """ DRAWING SECTION """
        # 1. Fill the background white so we have a clean slate every frame
        display.fill((255, 255, 255))

        # 2. Draw the grey rectangle where the numbers appear
        pygame.draw.rect(display,display_result_color,display_result)

        # 3. Draw a decorative line separating screen and buttons
        pygame.draw.line(display,display_result_color,(0,150), (500,150))

        ## 4. Draw all the button rectangles (The Grey Boxes)
        pygame.draw.rect(display,display_result_color,button1)
        pygame.draw.rect(display,display_result_color,button2)
        pygame.draw.rect(display,display_result_color,button3)

        pygame.draw.rect(display,display_result_color,button4)
        pygame.draw.rect(display,display_result_color,button5)
        pygame.draw.rect(display,display_result_color,button6)

        pygame.draw.rect(display,display_result_color,button7)
        pygame.draw.rect(display,display_result_color,button8)
        pygame.draw.rect(display,display_result_color,button9)

        # displaying the zeros
        pygame.draw.rect(display,display_result_color,button0)
        pygame.draw.rect(display,display_result_color,button00)
        pygame.draw.rect(display,display_result_color,button000)

        # displaying the operations
        pygame.draw.rect(display,display_result_color,button_plus)
        pygame.draw.rect(display,display_result_color,button_minus)
        pygame.draw.rect(display,display_result_color,button_times)
        pygame.draw.rect(display,display_result_color,button_divide)
        pygame.draw.rect(display,display_result_color,button_equals)

        # 5. Draw the text on top of the buttons ('blit' means copy pixels to screen)
        display.blit(text_surface1,text_rect1)
        display.blit(text_surface2,text_rect2)
        display.blit(text_surface3,text_rect3)

        display.blit(text_surface4,text_rect4)
        display.blit(text_surface5,text_rect5)
        display.blit(text_surface6,text_rect6)

        display.blit(text_surface7,text_rect7)
        display.blit(text_surface8,text_rect8)
        display.blit(text_surface9,text_rect9)

        display.blit(text_surface0,text_rect0)
        display.blit(text_surface00,text_rect00)
        display.blit(text_surface000,text_rect000)

        display.blit(text_surface_plus,text_rect_plus)
        display.blit(text_surface_minus,text_rect_minus)
        display.blit(text_surface_times,text_rect_times)
        display.blit(text_surface_divide,text_rect_divide)
        display.blit(text_surface_equals,text_rect_equals)

        # 6. Render the CURRENT INPUT (the numbers you typed)
        # We render it fresh every frame because the numbers change
        display_text = font.render(current_input, True, (0, 0, 0))

        # We place it slightly offset inside the result box
        display.blit(display_text, (display_result.x + 20, display_result.y + 30))

        # Draw Clear button and its text
        pygame.draw.rect(display, display_result_color, button_clear)
        display.blit(text_surface_clear, text_rect_clear)

        # Update the window title
        pygame.display.set_caption("CALCULATOR  ")

        # 7. Update the full display Surface to the screen
        pygame.display.update()

# Standard Python check to run main() only if this file is run directly
if __name__ == "__main__":
    main()