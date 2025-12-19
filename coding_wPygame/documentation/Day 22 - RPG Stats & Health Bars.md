Tags: [[Programming]], [[Python]], [[PyGame]], [[Game]]

---
### 1) Learning Goal

You will learn to create **Relative UI Elements**. Unlike the Inventory (which was a static list of boxes), a Health Bar is dynamic. You will use math to calculate the width of a rectangle based on player stats and build a Leveling System that scales difficulty.

### 2) Clear Overview

- **The Stats:** We add `hp`, `max_hp`, `xp`, and `level` to the Player.
- **The Visuals:** We use a **Ratio** to draw the bar.
    
    - `current_hp / max_hp` gives us a percentage (e.g., 0.5 for 50%).
    - We multiply the Bar's Max Width by that percentage.

- **The Feedback Loop:**
    
    - Gain XP -> Level Up -> Increase Max HP -> Bar looks smaller (visually) but holds more data.        

### 3) Deep Explanation

**A. The Health Bar Logic**

We don't hard code the width in pixels. We calculate it every frame based on the current stats.

$$Width = \text{TotalWidth} \times \left( \frac{\text{CurrentHP}}{\text{MaxHP}} \right)$$

**B. The Layering (UI Polish)**

Professional UI uses the "Sandwich" method (Painter's Algorithm):

1. **Background (Red):** Shows what you _lost_.
    
2. **Foreground (Green):** Shows what you _have_.
    
3. **Border (White):** Keeps it looking clean.
    

**C. Scaling Difficulty**

When leveling up, we don't just reset XP. We make the next level harder to reach by multiplying the requirement.

max_xp = max_xp * 1.5

### 4) Runnable Pygame Code Example

This code adds a UI system to a basic player.

- **SPACE:** Take Damage.
- **X:** Gain XP (Watch the bar fill and reset!).

``` Python
import pygame, sys

# 1. Setup
pygame.init()
SCREEN_W, SCREEN_H = 800, 600
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)
stat_font = pygame.font.SysFont("Arial", 16, bold=True)

# --- CLASSES ---
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 100, 255)) 
        self.rect = self.image.get_rect(center=(400, 300))
        
        # RPG STATS
        self.current_hp = 100
        self.max_hp = 100
        self.xp = 0
        self.max_xp = 50
        self.level = 1

    def take_damage(self, amount):
        self.current_hp -= amount
        if self.current_hp < 0: self.current_hp = 0

    def gain_xp(self, amount):
        self.xp += amount
        # Level Up Logic
        if self.xp >= self.max_xp:
            self.xp = 0
            self.level += 1
            self.max_xp = int(self.max_xp * 1.5) # Scale difficulty
            self.max_hp += 20
            self.current_hp = self.max_hp # Full heal
            print(f"Level Up! Now Level {self.level}")

# --- UI FUNCTION ---
def draw_interface(surface, player):
    # 1. SETUP
    bar_x, bar_y = 20, 20
    bar_w, bar_h = 200, 25
    
    # 2. CALCULATE RATIO
    # Avoid division by zero!
    if player.max_hp > 0:
        ratio = player.current_hp / player.max_hp
    else:
        ratio = 0
        
    fill_w = bar_w * ratio
    
    # 3. DRAW BAR LAYERS
    # Red Background
    pygame.draw.rect(surface, (100, 0, 0), (bar_x, bar_y, bar_w, bar_h))
    # Green Foreground
    pygame.draw.rect(surface, (0, 200, 50), (bar_x, bar_y, fill_w, bar_h))
    # White Border
    pygame.draw.rect(surface, (255, 255, 255), (bar_x, bar_y, bar_w, bar_h), 2)
    
    # 4. DRAW TEXT
    hp_text = stat_font.render(f"{player.current_hp}/{player.max_hp}", True, (255, 255, 255))
    surface.blit(hp_text, (bar_x + 70, bar_y + 4))
    
    xp_text = font.render(f"LVL: {player.level}   XP: {player.xp}/{player.max_xp}", True, (255, 255, 255))
    surface.blit(xp_text, (20, 60))

# --- MAIN LOOP ---
player = Player()

while True:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # TESTING INPUTS
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.take_damage(15)
            if event.key == pygame.K_x:
                player.gain_xp(20)

    # DRAWING
    screen.fill((30, 30, 30))
    
    # Draw Player
    pygame.draw.rect(screen, (0, 100, 255), player.rect)
    
    # Draw UI (Always last!)
    draw_interface(screen, player)
    
    # Hints
    hint = font.render("[SPACE] Damage   [X] Gain XP", True, (150, 150, 150))
    screen.blit(hint, (20, 550))

    pygame.display.update()
```

### 5) 20-Minute Drill

**Your Task:** Implement a **Mana Bar**.

1. Add `self.mana = 50` and `self.max_mana = 50` to the Player class.
    
2. In `draw_interface`, draw a **Blue Bar** directly below the XP text.
    
3. Add logic: Pressing **M** uses 10 Mana.
    
4. **Regeneration:** In the game loop, add `player.mana += 0.05` so it slowly refills over time.
    

### 6) Quick Quiz

1. **Why do we use a ratio (`current / max`) instead of pixels?**
    
2. **What happens if `current_hp` goes below 0 in our calculation?**
    
3. **Why is the UI drawn _after_ the player?**
    

**Answers:**

1. So the bar size works regardless of whether the player has 100 HP or 9000 HP.
    
2. Python handles it, but visually you might get a "negative width" error or a backwards bar depending on the math. It's best to clamp it: `max(0, current_hp)`.
    
3. **Painter's Algorithm**: We want the UI to float _on top_ of the game world.
    

### 7) Homework for Tomorrow

**Integrate Stats into your Day 21 Inventory.**

- Add a "Health Potion" to your inventory list.
    
- When used (removed from list), call `player.current_hp += 50`.
    
- Ensure it doesn't go over `player.max_hp`.
    

### 8) Progress to Mastery

🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜⬜⬜⬜⬜⬜⬜⬜ **73%**

---

### 9) Obsidian Note

## 🧠 CONCEPT SUMMARY

#### Relative UI Elements:
Unlike static inventory slots, a health bar is dynamic. We use a **Ratio** to decouple the *visual size* of the bar from the *actual numbers* of the stat.
> [!note] The Formula
> $$\text{Draw Width} = \text{Total Width} \times \left( \frac{\text{Current HP}}{\text{Max HP}} \right)$$

#### UI Layering (The Sandwich):
To create a readable bar, we draw three rectangles in a specific order (Painter's Algorithm):
1.  **Background:** Dark Red (shows missing HP).
2.  **Foreground:** Bright Green (shows remaining HP).
3.  **Border:** White/Black outline (separates UI from the game world).

#### Scaling Progression:
Leveling up shouldn't just reset the bar. It should increase difficulty. We use a multiplier (e.g., `1.5x`) so that Level 2 requires significantly more XP than Level 1.

---

## 🛠️ WHAT I DID TODAY

* **Created Player Stats:** Added `current_hp`, `max_hp`, `xp`, and `level` variables to the Player class.
* **Built a Dynamic Health Bar:** Implemented the 3-layer drawing logic using the ratio formula.
* **Implemented Leveling:** Wrote logic to trigger a "Level Up" event when XP fills the bar, resetting XP and boosting stats.
* **Added Text Feedback:** Overlayed font renders on top of the bars to show exact numbers (e.g., "50/100").

---

## 💻 SOURCE CODE

> [!example]- UI DRAW FUNCTION
> ```python
> def draw_ui(surface, player):
>     # 1. Calculate Ratio (0.0 to 1.0)
>     ratio = player.current_hp / player.max_hp
>     
>     # 2. Define Dimensions
>     BAR_W, BAR_H = 200, 25
>     fill_w = BAR_W * ratio
>     
>     # 3. Draw Layers
>     # Background (Red)
>     pygame.draw.rect(surface, (100, 0, 0), (20, 20, BAR_W, BAR_H))
>     # Foreground (Green)
>     pygame.draw.rect(surface, (0, 255, 0), (20, 20, fill_w, BAR_H))
>     # Border (White)
>     pygame.draw.rect(surface, (255, 255, 255), (20, 20, BAR_W, BAR_H), 2)
> ```

---

## 🧠 LEARNED TODAY

* **Visual Feedback:** A number (`HP: 50`) is informative, but a bar is *visceral*. Players react faster to a shrinking green bar than to reading text.
* **Clamping:** When calculating UI widths, it is important to prevent negative numbers if HP drops below 0 (e.g., using `max(0, hp)`).
* **Order of Operations:** UI functions must be called **after** `all_sprites.draw()` so they appear floating above the gameplay.

---

## 🎯 GOALS FOR TOMORROW

> [!todo] 🏃 **Day 23: Animation & Sprite Sheets**
> * Learn to load a "Sprite Sheet" (single image with multiple frames).
> * Create an `animate()` function using a list of images.
> * Make the player "walk" when moving and "idle" when stopped.
