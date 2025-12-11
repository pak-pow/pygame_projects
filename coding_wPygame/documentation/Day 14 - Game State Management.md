Tags: [[Programming]], [[Python]], [[PyGame]], [[Game]]

---
### 1) Learning Goal

You will learn to create a **Game State Manager**. This is a system that allows your game to switch between different "scenes" (Menu, Level 1, Game Over) without closing the window.

### 2) Clear Overview

- **The Problem:** You have one `while True` loop. How do you stop the player from moving when they are in the Menu?
    
- **The Solution:** A **State Machine**.
    
    - We create a variable: `game_state = "menu"`.
        
    - If `game_state == "menu"`: Draw buttons.
        
    - If `game_state == "playing"`: Update physics.
        
    - If `game_state == "game_over"`: Show final score.
        

### 3) Deep Explanation

**A. The Manager Class**

Instead of putting everything in main(), we make a class called GameStateManager.
It has a specific method for each state (e.g., run_menu(), run_game()).

**B. The Central Loop**

The main while loop becomes very simple. It just asks the manager: "What should I do right now?"

``` Python
if self.state == 'intro':
    self.intro()
elif self.state == 'main_game':
    self.main_game()
```

**C. State Transitions**

To switch screens, we simply change the variable.

- Click "Start Button" -> `self.state = 'main_game'`    
- Player HP hits 0 -> `self.state = 'game_over'`

### 4) Runnable Pygame Code Example

Here is a complete State Machine.

- **State 1 (Menu):** Press **SPACE** to Start.
- **State 2 (Game):** Click the **Blue Square** to win. (If you miss, nothing happens).    
- **State 3 (Game Over):** Press **R** to Restart.

If the `paused()` function just fills the screen with black, the game disappears.

**The Solution:** We separate the **Game Logic** (movement) from the **Game Drawing**

- **Running State:** Runs `Logic` + `Drawing`.
- **Paused State:** Runs `Drawing` (so you see the game) + `Overlay` (transparent dimming) + `Pause Menu`. It **skips** the Logic (so the cube stops).   

``` python
import pygame, sys

# 1. Setup
pygame.init()
SCREEN_W, SCREEN_H = 800, 600
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 40)

class GameStateManager:
    def __init__(self):
        self.state = 'intro'
        
        # Game Objects
        self.target_rect = pygame.Rect(400, 300, 50, 50)
        self.target_speed = 5
        
        # Create a Transparent Overlay Surface
        # We make a new surface the size of the screen
        self.overlay = pygame.Surface((SCREEN_W, SCREEN_H))
        self.overlay.fill((0, 0, 0)) # Fill black
        self.overlay.set_alpha(128)  # Set transparency (0=Invisible, 255=Opaque)

    # --- HELPER: JUST DRAW THE GAME ---
    # We pull this out so both 'main_game' and 'paused' can use it!
    def draw_game_elements(self):
        screen.fill((20, 20, 40)) # Clear screen
        pygame.draw.rect(screen, (0, 100, 255), self.target_rect)
        msg = font.render("CLICK THE SQUARE! (ESC to Pause)", True, (255, 255, 255))
        screen.blit(msg, (150, 50))

    # --- STATE 1: MENU ---
    def intro(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state = 'main_game'

        screen.fill((50, 50, 50))
        title = font.render("START MENU", True, (255, 255, 255))
        instr = font.render("Press SPACE to Play", True, (0, 255, 0))
        screen.blit(title, (300, 200))
        screen.blit(instr, (250, 300))

    # --- STATE 2: PLAYING ---
    def main_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.target_rect.collidepoint(event.pos):
                    self.state = 'game_over'
            
            # PAUSE TRIGGER
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = 'paused'

        # 1. GAME LOGIC (Movement)
        # This ONLY runs in 'main_game', not 'paused'
        self.target_rect.x += self.target_speed
        if self.target_rect.right > 800 or self.target_rect.left < 0:
            self.target_speed *= -1

        # 2. DRAWING
        self.draw_game_elements()

    # --- STATE 3: PAUSED ---
    def paused(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # UNPAUSE TRIGGER
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = 'main_game'

        # 1. DRAW THE GAME (Frozen)
        # We call the draw helper, but we skipped the logic above!
        self.draw_game_elements()
        
        # 2. DRAW OVERLAY
        # Blit the semi-transparent black surface on top
        screen.blit(self.overlay, (0, 0))
        
        # 3. DRAW PAUSE TEXT
        text = font.render("PAUSED", True, (255, 255, 255))
        rect = text.get_rect(center=(SCREEN_W//2, SCREEN_H//2))
        screen.blit(text, rect)

    # --- STATE 4: GAME OVER ---
    def game_over(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.state = 'intro'

        screen.fill((50, 0, 0))
        title = font.render("GAME OVER", True, (255, 255, 255))
        instr = font.render("Press R to Restart", True, (0, 255, 0))
        screen.blit(title, (300, 200))
        screen.blit(instr, (250, 300))

    def update(self):
        if self.state == 'intro':
            self.intro()
        elif self.state == 'main_game':
            self.main_game()
        elif self.state == 'paused':
            self.paused()
        elif self.state == 'game_over':
            self.game_over()

# --- MAIN LOOP ---
game_manager = GameStateManager()

while True:
    game_manager.update()
    pygame.display.update()
    clock.tick(60)
```

### 🧠 Changes Made:

1. **`draw_game_elements()`**: I extracted the drawing code so both `main_game` and `paused` can use it.
    
2. **`self.overlay`**: Created a black surface with `set_alpha(128)` to achieve the "dimmed" look.
    
3. **`paused()` Logic**:
    
    - Calls `draw_game_elements()` (shows the game).
        
    - **Skips** `self.target_rect.x += ...` (stops movement).
        
    - Blits `self.overlay` on top.

### 5) 20-Minute Drill

**Your Task:** Add a **Pause** state.

1. Add a new check in `update()`: `elif self.state == 'paused': self.paused()`.
2. Define the `paused()` method. It should just draw "PAUSED" text and wait for **P** to be pressed again.
3. Modify `main_game`: If the user presses **P**, switch state to `'paused'`.
4. Modify `paused`: If the user presses **P**, switch state back to `'main_game'`.

### 6) Quick Quiz

1. **Why do we put `pygame.event.get()` inside EACH state method instead of once in the main loop?**    
2. **Does switching from 'main_game' to 'paused' delete the player's variables?**
3. **How would you pass the score from the Game to the Game Over screen?**

**Answers:**

1. Because different screens need to handle inputs differently (e.g., Spacebar starts the game in Menu, but jumps in Game).
2. **No.** Because the `GameStateManager` class stays alive. The variables (`self.target_rect`) are stored in `self`, so they persist.
3. It's already there! Since `self.score` is part of the class, the `game_over` method can simply read `self.score` to display it.

### 7) Homework for Tomorrow

**Integrate this into Vertical Pong.**

- **Menu:** "Press Space to Pong".    
- **Game:** The actual game.
- **Game Over:** If the ball hits the bottom, switch to this screen. Display the final score. Press Space to play again.

### 8) Progress to Mastery

🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩 **46%**

### 9) Obsidian Note

# Day 14 – Game State Management

## 🧠 CONCEPT SUMMARY

#### The State Machine:
A design pattern where the game can only be in one "mode" at a time (Menu, Playing, Paused).

#### The Manager Class:
A central class that holds the data (Score, Player object) and decides which logic to run.

> [!note] 
> Instead of a messy `while True` loop, we have a clean `manager.update()`.
#### Implementing Pause: 
To pause a game but keep the graphics visible: 

1. Separate **Logic** (movement) from **Rendering** (drawing). 
2. In the `paused` state, call the **Rendering** function but **skip** the **Logic** lines. 
3. Draw a semi-transparent overlay (`set_alpha`) on top to indicate the paused state.
#### Persistence:
Because the Manager object stays alive for the entire program, variables stored in `self` (like Score or Player HP) are not lost when switching screens. This makes pausing or changing levels easy.

---
## 🛠️ WHAT I DID TODAY

* **Built a State Manager:** Created a class with `intro`, `game`, and `game_over` methods.
* **Handled Transitions:** Implemented logic to switch states based on events (Key press, Mouse click).
* **Isolated Inputs:** Learned that input handling must happen *inside* the specific state method so controls don't overlap (e.g., clicking 'Start' doesn't also shoot a gun).
* **Created a Loop:** Successfully built a flow: Menu -> Game -> End -> Menu.

---

## 💻 SOURCE CODE

> [!example]- STATE MANAGER STRUCTURE
> ```python
> class GameState:
>     def __init__(self):
>         self.state = 'menu'
> 
>     def menu(self):
>         # Draw Menu...
>         if key_pressed: self.state = 'game'
> 
>     def game(self):
>         # Run Physics...
>         if player_died: self.state = 'game_over'
> 
>     def update(self):
>         if self.state == 'menu':
>             self.menu()
>         elif self.state == 'game':
>             self.game()
> ```

> [!example]- PAUSE LOGIC
> ```python
> def main_game(self):
>     # Run Logic AND Draw
>     self.player.x += 1
>     self.draw_game()
> 
> def paused(self):
>     # Only Draw (Skip Logic)
>     self.draw_game()
>     # Draw Transparent Overlay
>     screen.blit(self.overlay, (0,0))
>     screen.blit(pause_text, (x,y))
> ```

---

## 🧠 LEARNED TODAY

* **Event Handling Placement:** If you call `pygame.event.get()` in the main loop, the sub-methods (menu/game) won't see any events because the main loop "ate" them. Call `event.get()` *inside* the active state method.
* **Refactoring:** This pattern removes all the clutter from the global scope. `main()` becomes just 3 lines of code.

---

## 🧪 PRACTICE / EXERCISES

**Exercise: Pause Logic**
Goal: Freeze the game without resetting variables.

```python
# In main_game()
if event.key == K_p:
    self.state = 'paused'

# In paused()
screen.fill((0,0,0))
text = font.render("PAUSED", True, WHITE)
screen.blit(text, (100, 100))
# Logic to unpause
if event.key == K_p:
    self.state = 'main_game'
````

---

## 🎯 GOALS FOR TOMORROW

> [!todo] 🗺️ **Day 15: Tilemaps & Level Editing**
> 
> - Learn to load grid-based levels from a text file or array.
>     
> - Create a parsing function to turn numbers (1, 2, 3) into Walls, Water, and Spikes.
>     
> - Build a proper platformer level.

