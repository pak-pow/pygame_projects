Tags: [[Python]], [[PyGame]], [[Game]], [[Programming]]

---

Welcome to **Day 7: UI & Text Rendering**.

Remember our Calculator project? We had to write `font.render`, `get_rect`, and `blit` about 20 times. It was painful. Today, we fix that. We are going to build a **Reusable UI System** so that we can create buttons and text labels with a single line of code.

#### 1) Learning Goal

We will learn how to create a `Button` class that handles its own text rendering and positioning, making it easy to build menus, scoreboards, and HUDs (Heads-Up Displays).

#### 2) Clear Overview

Text in Pygame is actually an **Image**.

1. **Rendering** (Turning string -> Image) is slow for the computer.
2. **Blitting** (Copying Image -> Screen) is fast.

**The Golden Rule:** Never call `font.render()` inside your main game loop unless the text changes (like a score). Render it once in `__init__`, save the image, and just blit that image in the loop.

#### 3) Deep Explanation

**A. The UI Element Class**

Instead of writing rect = ... and text = ... separately, we combine them into a class.

- **Attributes:** `image` (the rendered text), `rect` (position), `bg_color` (button background).
- **Methods:** `draw(screen)` handles the blitting.


**B. Centering Text**

- The hardest part of UI is centering text on a button.
- Pygame makes this easy with Rect alignment:

*text_rect.center = button_rect.center*

This snaps the center of the text directly to the center of the button background.

---

#### 4) Runnable Pygame Code Example

Here is a complete "Main Menu" example. Notice how clean the Game Loop is we create 3 buttons using a list, and the loop just draws them.

``` python
import pygame, sys

# 1. Setup
pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

# --- THE UI CLASS (The Blueprint) ---
class UIElement(pygame.sprite.Sprite):
    def __init__(self, text, x, y, width, height):
        super().__init__() 
        # 1. The Background Button (Visuals)
        self.image = pygame.Surface((width, height))
        self.image.fill((50, 50, 50)) # Dark Gray background
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # 2. The Text (Visuals)
        # Render text ONCE here, not in the loop!
        self.text_surf = font.render(text, True, (255, 255, 255)) # White text
        self.text_rect = self.text_surf.get_rect(center=self.rect.center) # Center on button

    def draw(self, surface):
        # Draw background rectangle
        surface.blit(self.image, self.rect)
        # Draw text on TOP of the rectangle
        # Note: text_rect is in global screen coordinates because we set it to match self.rect.center
        surface.blit(self.text_surf, self.text_rect)

# --- SETUP INSTANCES ---
# Create 3 buttons easily
btn_start = UIElement("START GAME", 200, 100, 200, 50)
btn_options = UIElement("OPTIONS", 200, 180, 200, 50)
btn_quit = UIElement("QUIT", 200, 260, 200, 50)

# Put them in a list to make management easy
ui_elements = [btn_start, btn_options, btn_quit]

# --- GAME LOOP ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        # Check for clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            # Check collisions with our handy class
            if btn_start.rect.collidepoint(mouse_pos):
                print("Start Game clicked!")
            elif btn_options.rect.collidepoint(mouse_pos):
                print("Options clicked!")
            elif btn_quit.rect.collidepoint(mouse_pos):
                print("Quitting...")
                pygame.quit()
                sys.exit()

    # Drawing
    screen.fill((0, 0, 0)) # Black background
    
    # Draw all UI elements with a simple loop
    for element in ui_elements:
        element.draw(screen)
        
    pygame.display.update()
```

---
#### 5) 20-Minute Drill

**Your Task:** Upgrade this Menu.

1. **Hover Effect:** Modify the `draw` method or the update logic. If the mouse is hovering over the button (`self.rect.collidepoint(pygame.mouse.get_pos())`), change the background color to **Blue**. If not hovering, keep it **Dark Gray**.

2. **Active Text:** Change the text of the "START GAME" button to say "LOADING..." when it is clicked. _(Hint: You will need to re-render the text surface)_.


---
#### 6) Quick Quiz

1. **Why is `font.render()` considered "expensive" or "slow"?**
    
2. **In the `UIElement` class, why do we blit `self.image` (the box) before `self.text_surf` (the words)?**
    
3. **To center text on a button, which Rect attributes do we align?**
    

**Answers:**

1. It has to calculate the shape of every letter pixel-by-pixel and create a new Surface in memory. Doing this 60 times a second causes lag.
    
2. Painter's Algorithm: If we drew the box second, it would cover up the words!
    
3. `text_rect.center = button_rect.center`.
    

---
#### 7) Homework for Tomorrow

Combine Day 6 and Day 7.

- Create a "Game Over" screen for your **Pong** or **Dodger** game.
    
- When the player loses, stop the game loop and draw a "GAME OVER" text and a "RESTART" button in the center of the screen.
    

---
#### 8) Progress to Mastery

🟩🟩🟩🟩🟩🟩🟩⬜⬜⬜ **23%**

---

#### 9) Obsidian Note

## 🧠 CONCEPT SUMMARY

#### Text Rendering Cost:
`font.render()` creates a new image (Surface) from a string. This is computationally heavy.

> [!note] 
> **Rule:** Render text once (in `__init__`) and save it. Only re-render if the text actually changes (like a score).

#### UI Classes:
Instead of managing separate variables for `rect` and `text_surface`, we create a `Button` or `UIElement` class.

> [!note] 
> This class holds the background rect, the text image, and handles the centering logic automatically.

#### Centering Text:
To place text perfectly in a box:
`text_rect = text_surface.get_rect()`
`text_rect.center = button_rect.center`

---

## 🛠️ WHAT I DID TODAY

* **Created a UI Class:** Built a `UIElement` class to encapsulate button logic.
* **Optimized Rendering:** Moved `font.render` into the `__init__` method to improve performance.
* **Implemented Menus:** Created a 3-button menu (Start, Options, Quit) using a simple list loop.
* **Handled Interactions:** Used `rect.collidepoint` inside the loop to detect button clicks.

---

## 💻 SOURCE CODE

> [!example]- SOURCE CODE
> ```python
> class Button:
>     def __init__(self, text, x, y, font):
>         # 1. Background
>         self.rect = pygame.Rect(x, y, 200, 50)
>         self.color = (50, 50, 50)
>         
>         # 2. Text (Rendered Once)
>         self.text_surf = font.render(text, True, (255, 255, 255))
>         self.text_rect = self.text_surf.get_rect(center=self.rect.center)
> 
>     def draw(self, screen):
>         pygame.draw.rect(screen, self.color, self.rect)
>         screen.blit(self.text_surf, self.text_rect)
>         
>     def check_click(self, pos):
>         return self.rect.collidepoint(pos)
> ```

---

## 🧠 LEARNED TODAY

* **Painter's Algorithm in UI:** Always draw the button background *before* blitting the text surface, otherwise the text is hidden.
* **Global vs Local Coordinates:** When using `blit`, the position you provide is where the top-left of the image goes on the *screen*. Aligning `rect.center` manages this math for you.

---

## 🧪 PRACTICE / EXERCISES

**Exercise: Hover Effect**
Goal: Change color when mouse is over button.

```python
# Inside Button.draw() or update()
mouse_pos = pygame.mouse.get_pos()
if self.rect.collidepoint(mouse_pos):
    self.color = (0, 0, 255) # Blue (Hover)
else:
    self.color = (50, 50, 50) # Gray (Normal)
````

---

## 🎯 GOALS FOR TOMORROW

> [!todo] 🚀 **Day 8: Movement & Velocity Vectors**
> 
> - Move beyond `x += 5`.
>     
> - Learn to use `pygame.math.Vector2` for professional movement.
>     
> - Implement "normalization" (solving the fast diagonal movement bug).

