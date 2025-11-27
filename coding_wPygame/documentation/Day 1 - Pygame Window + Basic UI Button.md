Tags: [[PyGame]], [[Game]], [[Python]], [[Programming]], [[Obsidian]]

---
## 🧠 CONCEPT SUMMARY

#### Initialization:
You must call `pygame.init()` after importing the module but before calling any other Pygame function.

> [!note] 
> This step loads the necessary hardware drivers to allow Pygame to talk to your computer.
#### The Game Loop:
Unlike standard scripts that run once and quit, games utilize an infinite `while True:` loop.

> [!note] 
> This loop constantly handles events, updates the game state, and draws to the screen to keep the game running.
#### Event Handling:
You must use `pygame.event.get()` to retrieve the list of inputs and iterate through them to handle specific actions like `QUIT`.

> [!note] 
> Pygame catches user inputs (keystrokes, clicks) and adds them to an event queue to keep the window responsive.

#### Rect Objects:
A `pygame.Rect` object represents a rectangular area defined by `(x, y, width, height)`.

> [!note] 
> Rect objects are crucial for positioning elements and handling collision detection (such as checking if a mouse cursor touched a button).

#### Double Buffering:
You must call `pygame.display.update()` to make any drawing changes (like `pygame.draw.rect`) visible to the user.

> [!note] 
> Drawing actually happens in a memory buffer first. The update function "flips" this buffer to the actual monitor so the changes appear on screen.

---
## WHAT I DID TODAY

- **Initialized the Engine:** Imported `pygame` and `sys`, and called `pygame.init()` to prepare the hardware.

- **Created the Window:** Set up a 500x400 display surface using `pygame.display.set_mode()`.

- **Built a UI Element:** Defined a `pygame.Rect` variable to act as a button and drew it using `pygame.draw.rect()`.

- **Implemented Event Logic:** Wrote a `for` loop to handle `QUIT` (closing the window) and `MOUSEBUTTONDOWN` (clicking).

- **Debugged Event Scope:** Fixed a logical bug where the button click code was outside the event loop, causing it to trigger repeatedly.

- **Added Interaction:** Programmed the button to toggle its color between Red and Blue upon being clicked using state-checking logic.

---
## SOURCE CODE

```python
# DAY 1 - Re-Understanding Pygame and its Functions  
# Book: Invent Your own computer games with python by Al Sweigart  
  
# Importing the essentials  
import pygame , sys  
from pygame.locals import *  
  
# initializing the pygame  
pygame.init()  
  
# Setting the window into 500 pixels in width and 400 in height  
# We store this in the variable 'screen' so we can draw on it later.  
screen = pygame.display.set_mode((500, 400))  
  
# Create a Rect object to represent our button.  
# Arguments are: (left_x, top_y, width, height)  
button_rect = pygame.Rect(100, 100, 200, 50)  
  
# setting the background color of the said rectangle  
# Define the initial color to be variable (Red)  
color = (255, 0, 0)  
  
# The Game Loop  
# This infinite loop runs continuously to keep the game running.  
while True:  
  
    # pygame.event.get() grabs a list of all input actions (clicks, keys)  
    # that happened since the last frame. We loop through them one by one.    for event in pygame.event.get():  
  
        # Check if the user clicked the 'X' button on the window  
        if event.type == QUIT:  
  
            # Unload pygame modules  
            pygame.quit()  
  
            # Close the python script completely  
            sys.exit()  
  
        # Check if the user clicked the mouse button AND if the mouse cursor  
        # was inside the button's rectangle area.        
        
        if event.type == MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):  
            print("Button was clicked!")  
  
            # Toggle Logic: Check the *current* color to decide the *next* color.  
            # If it is currently Blue...            
            
            if color == (0, 0, 255):  
            
                # ...change it to Red  
                color = (255, 0, 0)  
  
            # Otherwise (if it is Red)..  
            else:  
  
                # ...change it to Blue  
                color = (0, 0, 255)  
  
    # Fill the background with White to erase the previous frame's drawings.  
    # Without this, moving objects would leave a "trail".    screen.fill((255, 255, 255))  
  
    # Draw the button rectangle on the 'screen' surface using the current 'color'.  
    pygame.draw.rect(screen, color, button_rect)  
  
    # Set the window title  
    pygame.display.set_caption("TEST PYGAME  ")  
  
    # This flips the memory buffer to the actual screen so the user sees the changes.  
    pygame.display.update()

```

---
### 🧠 Learned Today

- **Scope Matters:** Event-specific logic (like checking `event.pos` or `event.type`) must live **inside** the `for event in pygame.event.get():` loop. If placed outside, it checks stale data every single frame (60+ times a second), leading to bugs.
    
- **State Toggling:** To switch between two states (Red/Blue), check the _current_ value in an `if/else` block before assigning the new value.
    
- **Tuples for Colors:** Colors in Pygame are defined as Tuples of three integers: `(Red, Green, Blue)`, ranging from 0 to 255.
    

---
## 🧪 Practice / Exercises

Exercise 1: The "Green Square" Popup
Goal: Draw a small green square at (50, 50) ONLY when the button is currently Blue.

``` python
# Place this inside the Drawing section of your loop (after screen.fill)
if color == (0, 0, 255):
    # Draw a green rect at x=50, y=50, w=20, h=20
    pygame.draw.rect(screen, (0, 255, 0), (50, 50, 20, 20))

```

Exercise 2: The "Escape Key" Exit
Goal: Close the game cleanly if the user presses the 'Esc' key.

``` python
# Place this inside the 'for event' loop
if event.type == KEYDOWN:
    if event.key == K_ESCAPE:
        pygame.quit()
        sys.exit()

```

---

## 💡 Notes to Self

> [!important] Order of Operations: 
> Always call `pygame.init()` before setting up the display.

> [!important] Coordinate System: 
> The top-left corner is (0, 0). X increases to the right, Y increases going down.

> [!important] Rect Collision: 
> 
> Use `my_rect.collidepoint((x, y))` to see if a specific point is inside a rectangle. This is the basis of clicking things in UI.

> [!important] Color Definitions: 
> 
> It is helpful to define colors as constants at the top of the file (e.g., `RED = (255, 0, 0)`) to make the code readable4.

---
## 🎯 Goals for Tomorrow

> [!todo] 🎨 **Day 2: Drawing Shapes & Images**
> - Learn to draw Circles, Lines, and Polygons.
> - Load external image files (`pygame.image.load`) to use as sprites.
> - Understand the `blit()` method to copy images onto the screen.

