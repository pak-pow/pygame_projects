Tags: [[Programming]], [[Python]], [[PyGame]], [[Game]]

---
#### 1) Learning Goal

We will learn to control the speed of our game loop using `pygame.time.Clock` and understand how to use **Delta Time** to make your game run at the same speed on _any_ computer (fast or slow).
#### 2) Clear Overview

Right now, on every game we did our `while True:` loop runs as fast as the CPU allows.

- **Fast PC:** The loop runs 2000 times a second. Your character flies off the screen instantly.
    
- **Slow PC:** The loop runs 30 times a second. Your character moves in slow motion.

We fix this by introducing a **Clock** to limit the Frame Rate (FPS) and using **Delta Time** to calculate movement based on _time_ rather than _frames_.

#### 3) Deep Explanation

**A. The Clock Object**

Pygame has a tool to manage time: pygame.time.Clock.

We create one before the loop: clock = pygame.time.Clock().

Inside the loop, we call clock.tick(60). This tells Pygame: "If this loop finishes early, sleep until 1/60th of a second has passed." This caps your game at 60 FPS.

**B. What is Delta Time (dt)?**

Even with a clock, FPS can fluctuate (lag). To fix this, we use Delta Time.

- **Delta Time (`dt`)** is the amount of time (in seconds) that passed since the last frame.
- If the game lags and the frame takes longer, `dt` gets bigger.
- If the game is fast, `dt` gets smaller.    

**C. The Magic Formula**

Instead of saying *"Move 5 pixels per frame"* we say *"Move 300 pixels per second."*

To do this in code, we multiply speed by dt:

($position += speed * dt$)

- **Normal Frame (0.016s):** Move $300 \times 0.016 = 4.8$ pixels. 
- **Laggy Frame (0.1s):** Move $300 \times 0.1 = 30$ pixels (the object "jumps" forward to catch up!).

#### 4) Runnable Pygame Code Example

This code runs a "race" between two squares.

- **Red Square:** Moves 5 pixels per **frame** (Bad! Speed depends on FPS).
- **Blue Square:** Moves 300 pixels per **second** (Good! Uses Delta Time).

Try changing the `FPS` variable to 30, then 60, then 120. Watch what happens to the Red square vs the Blue square.

``` python
import pygame, sys

# 1. Setup
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Day 4: FPS & Delta Time")

# Create the Clock object
clock = pygame.time.Clock()

# 2. Variables
FPS = 60  # Try changing this to 30 or 120 later!

# Red Square (Frame-based movement)
red_rect = pygame.Rect(50, 100, 50, 50)
red_speed_per_frame = 5 

# Blue Square (Time-based movement / Delta Time)
blue_rect = pygame.Rect(50, 250, 50, 50)
blue_speed_per_second = 300 # Pixels per second
blue_pos_x = 50.0 # We need a float variable for precision!

while True:
    # A. Calculate Delta Time (dt)
    # clock.tick(FPS) pauses the loop to maintain FPS.
    # It returns the time in milliseconds since the last frame.
    # We divide by 1000 to convert milliseconds to seconds (standard for dt).
    dt = clock.tick(FPS) / 1000

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Reset Race on Spacebar
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                red_rect.x = 50
                blue_rect.x = 50
                blue_pos_x = 50.0

    # --- LOGIC ---
    
    # 1. Move Red (Frame-based)
    # Moves 5 pixels every loop. If FPS is high, it zooms. If FPS is low, it crawls.
    red_rect.x += red_speed_per_frame
    
    # 2. Move Blue (Delta Time)
    # Moves 300 pixels * fraction of a second.
    # If FPS is 60, dt is 0.016. Move is 4.8 pixels.
    # If FPS is 30, dt is 0.033. Move is 9.9 pixels.
    # The speed remains constant regardless of FPS!
    blue_pos_x += blue_speed_per_second * dt
    blue_rect.x = int(blue_pos_x) # Update rect (must be int)

    # Boundary Wrap (Loop around screen)
    if red_rect.left > 600: red_rect.right = 0
    if blue_rect.left > 600: blue_pos_x = -50

    # --- DRAWING ---
    screen.fill((0, 0, 0))
    
    pygame.draw.rect(screen, (255, 0, 0), red_rect) # Red
    pygame.draw.rect(screen, (0, 0, 255), blue_rect) # Blue
    
    # Display FPS in caption
    pygame.display.set_caption(f"FPS: {int(clock.get_fps())} | DT: {dt:.4f}")
    
    pygame.display.update()
```

---

#### 5) 20-Minute Drill

**Your Task:** Modify the code above to verify how robust Delta Time is.

1. Change the `FPS` variable to **30**. Run it. Notice how the Red square slows down, but the Blue square keeps the same real-world speed.
2. Change the `FPS` variable to **120**. Run it. The Red square should be super fast; the Blue square should be normal.
3. **Coding Challenge:** Add a **Green Square** that moves vertically (down) at **200 pixels per second** using Delta Time.

_Do this now to prove to yourself why we use Delta Time._

---

#### 6) Quick Quiz

1. *What does `clock.tick(60)` do?*
2. *If `dt` is 0.5 (half a second) and your speed is 100, how far does the object move in that frame?*
3. *Why do we use a float variable (`blue_pos_x`) for the Blue square instead of just `blue_rect.x`?*

**Answers:**

1. It pauses the program just long enough to ensure the loop doesn't run faster than 60 times per second.
2. 50 pixels ($100 \times 0.5$).
3. `Rect` coordinates are integers (whole numbers). `dt` calculations result in decimals (like 4.8). If we stored 4.8 in a rect, it would round down to 4 every time, losing speed. We track the float separately for accuracy.

---
#### 7) Homework for Tomorrow

Taking our **Day 3** code (the moving square with physics) and upgrade it:

1. Add `clock = pygame.time.Clock()` and `dt`.
2. Convert your velocity variables to use "Pixels Per Second".    
3. Multiply your velocity by `dt` when adding to `x` and `y`.

---
#### 8) Progress to Mastery

🟩🟩🟩🟩⬜⬜⬜⬜⬜⬜ **13%**

---
#### 9) Obsidian Note

# 🧠 CONCEPT SUMMARY

### **Frame Rate (FPS)**

How many times the game loop updates per second.  
Higher FPS → smoother gameplay.

⚠️ **Uncapped FPS** = 100% CPU usage + unpredictable game speed.

---
### **The Clock**

`pygame.time.Clock()` is used to **monitor and limit FPS**.

> [!note]  
> `clock.tick(60)` means:  
> **“Wait until 1/60th of a second has passed since the last frame.”**

---
### **Delta Time (dt)**

The time (in **seconds**) between this frame and the previous frame.

> [!note] Formula:  
> `dt = clock.tick(FPS) / 1000`

(Pygame returns milliseconds → divide by 1000 to convert to seconds.)

---
### **Framerate Independence**

Movement should depend on **time**, not **frames**.

> [!important]  
> ❌ Wrong:  
> `x += 5` → 5 pixels _per frame_, varies with FPS
> 
> ✅ Right:  
> `x += 300 * dt` → 300 pixels _per second_, same speed on all machines

---
## 🛠️ **WHAT I DID TODAY**

- **Controlled FPS** using `clock.tick()`    
- **Calculated delta time** in seconds
- **Implemented time-based movement** using `Pixels Per Second`
- **Visualized the difference** between frame-based vs time-based motion

---
## 💻 SOURCE CODE

> [!example]- **Source Code**
> ```python
> import pygame, sys
> pygame.init()
> 
> screen = pygame.display.set_mode((600, 400))
> clock = pygame.time.Clock()
> FPS = 60
> 
> # Use floats when using dt!
> pos_x = 0.0
> SPEED_PER_SECOND = 300
> 
> rect = pygame.Rect(0, 200, 50, 50)
> 
> while True:
>     # 1. Calculate dt (seconds since last frame)
>     dt = clock.tick(FPS) / 1000
> 
>     for event in pygame.event.get():
>         if event.type == pygame.QUIT:
>             pygame.quit()
>             sys.exit()
> 
>     # 2. Move based on Time
>     pos_x += SPEED_PER_SECOND * dt
> 
>     # 3. Update Rect (convert float → int)
>     rect.x = int(pos_x)
> 
>     # Draw
>     screen.fill((0, 0, 0))
>     pygame.draw.rect(screen, (0, 255, 255), rect)
>     pygame.display.update()
> ```

## 🧠 LEARNED TODAY

### Float Precision

`pygame.Rect` only stores **integers**, but dt creates **decimal movement** (like 0.4 pixels).  
To avoid losing precision, store position in a **float variable**, then convert back.

### Lag Compensation

If your PC lags:

- dt becomes **larger**
    
- object moves **more per frame**
    

This keeps motion consistent over time.

---
#### 🧪 SIDE PROJECT: VERTICAL PONG

A mini-game using:

- Delta Time physics
- Float positions
- Collision detection
- Paddle + ball movement

> [!example] PROJECT SOURCE CODE
> 
> ```python
> """
> PONG GAME — TO-DO LIST
> ----------------------
> 
> 📌 STAGE 1 — BASE SETUP
>     - Create window [DONE]
>     - Init Pygame, Clock(), dt [DONE]
>     - Game loop [DONE]
>     - Clear + update screen [DONE]
> 
> 📌 STAGE 2 — OBJECT CREATION
>     - Create paddle [DONE]
>     - Create ball [DONE]
>     - Paddle speed (px/s) [DONE]
>     - Ball speed + direction vector [PARTIAL]
> 
> 📌 STAGE 3 — PADDLE MOVEMENT
>     - Player movement
>     - Use delta time
>     - Boundary checks
> 
> 📌 STAGE 4 — BALL PHYSICS
>     - Move ball using dt
>     - Wall collisions
>     - Paddle collisions
>     - Ball speed increase (optional)
> 
> 📌 STAGE 5 — SCORING SYSTEM
>     - Detect out-of-bounds
>     - Player scoring
>     - Reset ball
>     - Serve direction
> 
> 📌 STAGE 6 — POLISH
>     - Center line
>     - Score text
>     - Restart on SPACE
>     - Sounds (optional)
> 
> 📌 STAGE 7 — EXTRA FEATURES
>     - Difficulty
>     - AI
>     - Paddle acceleration
>     - Color themes
>     - FPS + dt debug
>     - Main menu
> """
> 
> 
> # ================================= MAIN CODE ===================================
> 
> import pygame
> import sys
> import pygame.font
> import random
> from pygame.locals import *
> from pygame.time import Clock
> 
> def main():
> 
>     pygame.init()
> 
>     # Font
>     font = pygame.font.SysFont(None, 32)
> 
>     # Display
>     WINDOW_WIDTH = 600
>     WINDOW_HEIGHT = 700
>     DISPLAY = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
> 
>     # Clock
>     clock = Clock()
>     FPS = 60
> 
>     # Player paddle
>     PLAYER_OBJ = pygame.Rect(200, 600, 200, 25)
>     PLAYER_speed_per_second = 500
>     PLAYER_pos_x = float(PLAYER_OBJ.x)
> 
>     # Ball
>     ball_started = False
>     BALL_OBJ = pygame.Rect(200, 100, 30, 30)
> 
>     BALL_SPEED_X = 0.0
>     BALL_SPEED_Y = 500.0
> 
>     BALL_POS_X = float(BALL_OBJ.x)
>     BALL_POS_Y = float(BALL_OBJ.y)
> 
>     # Colors
>     PLAYER_COLOR = (0, 0, 0)
>     BALL_COLOR = (0, 0, 0)
> 
>     # Movement flags
>     M_left = False
>     M_right = False
> 
>     while True:
> 
>         dt = clock.tick(FPS) / 1000
> 
>         for event in pygame.event.get():
> 
>             if event.type == QUIT:
>                 pygame.quit()
>                 sys.exit()
> 
>             if event.type == KEYDOWN:
> 
>                 if event.key in (K_LEFT, K_a):
>                     M_left = True
> 
>                 if event.key in (K_RIGHT, K_d):
>                     M_right = True
> 
>             if event.type == KEYUP:
> 
>                 if event.key in (K_LEFT, K_a):
>                     M_left = False
> 
>                 if event.key in (K_RIGHT, K_d):
>                     M_right = False
> 
>         # Paddle movement
>         if M_left:
>             PLAYER_pos_x -= PLAYER_speed_per_second * dt
> 
>         if M_right:
>             PLAYER_pos_x += PLAYER_speed_per_second * dt
> 
>         PLAYER_OBJ.x = int(PLAYER_pos_x)
> 
>         # Boundary
>         if PLAYER_OBJ.left < 0:
>             PLAYER_OBJ.left = 0
>             PLAYER_pos_x = float(PLAYER_OBJ.x)
> 
>         if PLAYER_OBJ.right > WINDOW_WIDTH:
>             PLAYER_OBJ.right = WINDOW_WIDTH
>             PLAYER_pos_x = float(PLAYER_OBJ.x)
> 
>         # Ball movement
>         BALL_POS_X += BALL_SPEED_X * dt
>         BALL_POS_Y += BALL_SPEED_Y * dt
> 
>         BALL_OBJ.x = int(BALL_POS_X)
>         BALL_OBJ.y = int(BALL_POS_Y)
> 
>         # Wall collisions
>         if BALL_OBJ.top <= 0:
>             BALL_SPEED_Y *= -1
>             BALL_OBJ.top = 0
>             BALL_POS_Y = float(BALL_OBJ.y)
> 
>         if BALL_OBJ.left <= 0:
>             BALL_OBJ.left = 0
>             BALL_SPEED_X *= -1
> 
>         elif BALL_OBJ.right >= WINDOW_WIDTH:
>             BALL_OBJ.right = WINDOW_WIDTH
>             BALL_SPEED_X *= -1
> 
>         BALL_POS_X = float(BALL_OBJ.x)
> 
>         # Paddle collision
>         if BALL_OBJ.colliderect(PLAYER_OBJ):
> 
>             BALL_SPEED_Y *= -1
>             BALL_OBJ.bottom = PLAYER_OBJ.top
>             BALL_POS_Y = float(BALL_OBJ.y)
> 
>             offset = BALL_OBJ.centerx - PLAYER_OBJ.centerx
>             BALL_SPEED_X += offset * 5
> 
>             if not ball_started:
>                 BALL_SPEED_X = random.choice([-200.0, -150.0, 150.0, 200.0])
>                 ball_started = True
> 
>         # Reset ball
>         if BALL_OBJ.bottom >= WINDOW_HEIGHT:
> 
>             BALL_OBJ.x = WINDOW_WIDTH // 2
>             BALL_OBJ.y = 100
> 
>             BALL_POS_X = float(BALL_OBJ.x)
>             BALL_POS_Y = float(BALL_OBJ.y)
> 
>             BALL_SPEED_X = 0
>             BALL_SPEED_Y = 400.0
> 
>             ball_started = False
> 
>         # Render
>         DISPLAY.fill((255, 255, 255))
> 
>         # FPS
>         text_surface = font.render(f"FPS: {int(clock.get_fps())}", True, (0, 0, 0))
>         DISPLAY.blit(text_surface, (10, 10))
> 
>         pygame.draw.rect(DISPLAY, PLAYER_COLOR, PLAYER_OBJ)
>         pygame.draw.rect(DISPLAY, BALL_COLOR, BALL_OBJ)
> 
>         pygame.display.update()
> 
> 
> if __name__ == "__main__":
>     main()
> ```
> 
> 
> 

---
## 💡 NOTES TO SELF

> [!important]  
> `clock.tick()` returns **milliseconds**.  
> Dividing by **1000** converts them to **seconds**, which is required for physics math like:  
> `distance = speed * time`.

---
## 🎯 GOALS FOR TOMORROW

> [!todo] **Day 5 — Sprites & Classes**
> - Learn OOP for games
> - Create a `Player` class
> - Use `pygame.sprite.Sprite` to handle objects efficiently 

---
