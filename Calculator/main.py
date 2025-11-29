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
    font = pygame.font.SysFont(None, 40)
    display = pygame.display.set_mode((500,700))

    # Adding a variable called current input
    current_input = ""

    # making the display result screen and more or
    # less like the seeing the number
    display_result = pygame.Rect(25,25,450,100)
    display_result_color = (217, 217, 217)

    # buttons for the 1-9
    button1 = pygame.Rect(25,180,80,100)
    button2 = pygame.Rect(125,180,80,100)
    button3 = pygame.Rect(225,180,80,100)

    button4 = pygame.Rect(25,300,80,100)
    button5 = pygame.Rect(125,300,80,100)
    button6 = pygame.Rect(225,300,80,100)

    button7 = pygame.Rect(25,420,80,100)
    button8 = pygame.Rect(125,420,80,100)
    button9 = pygame.Rect(225,420,80,100)

    # buttons for 0s
    button0 = pygame.Rect(25,540,80,100)
    button00 = pygame.Rect(125,540,80,100)
    button000 = pygame.Rect(225,540,80,100)

    # buttons for operations
    button_plus = pygame.Rect(325,180,60,180)
    button_minus = pygame.Rect(400,180,60,180)
    button_times = pygame.Rect(325,380,60,180)
    button_divide = pygame.Rect(400,380,60,180)
    button_equals = pygame.Rect(325,580,135,60)

    # button clear
    button_clear = pygame.Rect(25, 133, 80, 40)

    # rendering the text
    text_surface1 = font.render("1", True, (0,0,0))
    text_rect1 = text_surface1.get_rect(center = button1.center)

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

    text_surface0 = font.render("0", True, (0, 0, 0))
    text_rect0 = text_surface0.get_rect(center=button0.center)

    text_surface00 = font.render("00", True, (0, 0, 0))
    text_rect00 = text_surface00.get_rect(center=button00.center)

    text_surface000 = font.render("000", True, (0, 0, 0))
    text_rect000 = text_surface000.get_rect(center=button000.center)

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

    while True:

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN and button_clear.collidepoint(event.pos):
                current_input = ""
                print("CLEAR")

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

            if event.type == MOUSEBUTTONDOWN and button_plus.collidepoint(event.pos):
                current_input += "+"

            if event.type == MOUSEBUTTONDOWN and button_minus.collidepoint(event.pos):
                current_input += "-"

            if event.type == MOUSEBUTTONDOWN and button_times.collidepoint(event.pos):
                current_input += "*"

            if event.type == MOUSEBUTTONDOWN and button_divide.collidepoint(event.pos):
                current_input += "/"

            if event.type == MOUSEBUTTONDOWN and button_equals.collidepoint(event.pos):

                try:
                    current_input = str(eval(current_input))

                except :
                    current_input = "ERROR"

        display.fill((255, 255, 255))

        # now drawing the display screen
        pygame.draw.rect(display,display_result_color,display_result)

        # drawing the line that separates the screen and the buttons
        pygame.draw.line(display,display_result_color,(0,150), (500,150))

        # drawing the buttons from 1-9
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

        # displaying the texts
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

        # Displaying the numbers in the display result
        display_text = font.render(current_input, True, (0, 0, 0))
        display.blit(display_text, (display_result.x + 20, display_result.y + 30))

        pygame.draw.rect(display, display_result_color, button_clear)
        display.blit(text_surface_clear, text_rect_clear)

        pygame.display.set_caption("CALCULATOR  ")
        pygame.display.update()

if __name__ == "__main__":
    main()