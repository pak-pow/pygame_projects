Tags: [[Programming]], [[Python]], [[PyGame]], [[Game]]

---
Today we stop hard-coding rectangles (`Rect(100, 200...)`) and start **designing** levels. We will use a "Map" (a grid of text) and write a script that reads it and builds the world for us.
### 1) Learning Goal

You will learn to convert a 2D array (a list of text strings) into a playable game level by "parsing" the grid and placing sprites automatically.
### 2) Clear Overview

- **The Old Way:** Manually typing coordinates for every platform. Slow. Painful.
    
- **The New Way:** You draw the level using characters in a list.
    
    - `'X'` = Wall
    - `'P'` = Player Spawn
    - `' '` (Space) = Empty Air
    
- **The Parser:** A generic loop that reads the list.
    
    - Row 0, Col 0 is 'X'? -> Place a Wall at `(0, 0)`. 
    - Row 2, Col 5 is 'X'? -> Place a Wall at `(5 * 64, 2 * 64)`.


### 3) Deep Explanation

**A. The Map Data**

We represent the level as a list of strings:

Python

```
level_map = [
    'XXXXXXXXXX',
    'X        X',
    'X  P     X',
    'XXXXXXXXXX'
]
```

**B. The Grid Loop**

We need a nested loop (loop inside a loop).

1. Outer Loop: `enumerate(level_map)` gives us the **Row Index (Y)**.
2. Inner Loop: `enumerate(row)` gives us the **Column Index (X)**.

**C. The Math**

To find the pixel position:

- `pixel_x = col_index * TILE_SIZE`
- `pixel_y = row_index * TILE_SIZE`

---

### 4) Runnable Pygame Code Example

Here is a complete Platformer.

- **White Blocks:** Walls (`X`).    
- **Red Block:** Player (`P`).
- **Blue Blocks:** Water (`W`).

You can edit the `LEVEL_MAP` variable to redesign the level instantly!

``` python
import pygame, sys

# ----------------------------------------
# 1. Setup
# ----------------------------------------
pygame.init()
SCREEN_W, SCREEN_H = 600, 400
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()
TILE_SIZE = 40
pygame.display.set_caption("Platformer Demo")

# ----------------------------------------
# LEVEL (ASCII ART)
# ----------------------------------------
LEVEL_MAP = [
    'XXXXXXXXXXXXXXX',
    'X             X',
    'X P           X',
    'X      XXX    X',
    'X             X',
    'XXXX       XXXX',
    'X             X',
    'X    WWWWW    X',
    'XXXXXXXXXXXXXXX'
]

# ----------------------------------------
# CLASSES
# ----------------------------------------
class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        
        # Colors for different tile types
        if type == 'X':
            self.image.fill((180, 180, 180))   # Wall
            pygame.draw.rect(self.image, (80, 80, 80), (0, 0, TILE_SIZE, TILE_SIZE), 3)
        elif type == 'W':
            self.image.fill((30, 30, 200))     # Water
            pygame.draw.rect(self.image, (10, 10, 100), (0, 0, TILE_SIZE, TILE_SIZE), 3)

        self.rect = self.image.get_rect(topleft=pos)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, walls):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 100, 100))
        pygame.draw.rect(self.image, (200, 50, 50), (0, 0, 30, 30), 3)

        self.rect = self.image.get_rect(topleft=pos)
        self.walls = walls

        # Movement physics
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(0, 0)
        self.speed = 250
        self.gravity = 900
        self.jump_force = -500

        # Double jump
        self.can_double = True
        self.grounded = False

    def horizontal_movement(self, dt):
        keys = pygame.key.get_pressed()
        self.vel.x = 0

        if keys[pygame.K_LEFT]:
            self.vel.x = -self.speed
        if keys[pygame.K_RIGHT]:
            self.vel.x = self.speed

        # Move horizontally
        self.pos.x += self.vel.x * dt
        self.rect.x = round(self.pos.x)

        # Horizontal collisions
        hits = pygame.sprite.spritecollide(self, self.walls, False)
        for tile in hits:
            if self.vel.x > 0:
                self.rect.right = tile.rect.left
            elif self.vel.x < 0:
                self.rect.left = tile.rect.right
            self.pos.x = self.rect.x

    def vertical_movement(self, dt):
        keys = pygame.key.get_pressed()

        # Apply gravity
        self.vel.y += self.gravity * dt
        self.vel.y = min(self.vel.y, 900)   # Clamp fall speed

        # Move vertically
        self.pos.y += self.vel.y * dt
        self.rect.y = round(self.pos.y)

        # Vertical collision
        hits = pygame.sprite.spritecollide(self, self.walls, False)
        self.grounded = False

        for tile in hits:
            if self.vel.y > 0:  # Falling
                self.rect.bottom = tile.rect.top
                self.pos.y = self.rect.y
                self.vel.y = 0
                self.grounded = True
                self.can_double = True  # Reset double jump

            elif self.vel.y < 0:  # Hitting ceiling
                self.rect.top = tile.rect.bottom
                self.pos.y = self.rect.y
                self.vel.y = 0

        # Jumping logic
        if keys[pygame.K_SPACE]:
            if self.grounded:
                self.vel.y = self.jump_force
            elif self.can_double:
                self.vel.y = self.jump_force
                self.can_double = False

    def update(self, dt):
        self.horizontal_movement(dt)
        self.vertical_movement(dt)


# ----------------------------------------
# LEVEL PARSING
# ----------------------------------------
tile_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

for row_index, row in enumerate(LEVEL_MAP):
    for col_index, char in enumerate(row):

        x = col_index * TILE_SIZE
        y = row_index * TILE_SIZE

        if char in ('X', 'W'):
            tile = Tile((x, y), char)
            tile_group.add(tile)

        elif char == 'P':
            player = Player((x, y), tile_group)
            player_group.add(player)

# ----------------------------------------
# GAME LOOP
# ----------------------------------------
while True:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((20, 20, 20))

    tile_group.draw(screen)
    player_group.update(dt)
    player_group.draw(screen)

    pygame.display.update()

```

---

### 5) 20-Minute Drill

**Your Task:** Add **Lava** (`L`) to the level editor.

1. **Modify the Map:** Add some `'L'` characters to the bottom of the `LEVEL_MAP`.
2. **Update Tile Class:** Add logic in `Tile.__init__`: `if type == 'L': color = Red`.
3. **Add Danger Logic:** Inside the Player's update loop, check for collision with Lava tiles.
    
    - _Hint:_ You can check `tile.type` if you saved it, or just make a separate `lava_group`.
    - If the player touches Lava, reset their position to the start `(100, 200)`.

---

### 6) Quick Quiz

1. **If `TILE_SIZE` is 32, what is the pixel X coordinate of the 10th column?**
    
2. **Why do we need nested loops (`for row... for col...`) to read the map?**
    
3. **Why is this better than writing `Tile(100, 100)`, `Tile(140, 100)` manually?**
    

**Answers:**

1. 320 (`10 * 32`).
    
2. Because the map is 2D grid data. We need to go down the rows, and for each row, go across the columns.
    
3. Speed and Editability. You can redesign the whole level in 5 seconds just by editing the string list.
    

---

### 7) Homework for Tomorrow

Combine **Day 11 (Camera)** with **Day 15 (Tilemaps)**.

- Make your `LEVEL_MAP` huge (like 50 columns wide).
- Add the `CameraGroup` logic from Day 11.
- Now you have a side-scrolling platformer level!

---

### 8) Progress to Mastery

🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩 **50%** (HALF WAY THERE!)

---

### 9) Obsidian Note

## 🧠 CONCEPT SUMMARY

#### The Tilemap:
A grid-based approach to level design. Instead of placing objects at arbitrary pixels, we snap them to a grid.

#### ASCII Maps:
Using a list of strings to represent the level layout.
* `'X'` = Wall
* `' '` = Air
* `'P'` = Player

#### The Parsing Formula:
To turn grid coordinates into screen coordinates:
> [!note] 
> `x = col_index * TILE_SIZE`
> `y = row_index * TILE_SIZE`

---

## 🛠️ WHAT I DID TODAY

* **Created a Level Map:** Defined a layout using a Python list of strings.
* **Built a Parser:** Wrote a nested `for` loop to iterate through rows and columns.
* **Instantiated Tiles:** Created `Tile` objects automatically based on the character found in the map string.
* **Handled Spawning:** Used the map to spawn the Player (`P`) at a specific location without hard-coding coordinates.

---

## 💻 SOURCE CODE

> [!example]- LEVEL PARSER
> ```python
> LEVEL_MAP = [
>     'XXXXXXXXXX',
>     'X P      X',
>     'XXXXXXXXXX'
> ]
> 
> for row_idx, row in enumerate(LEVEL_MAP):
>     for col_idx, char in enumerate(row):
>         x = col_idx * TILE_SIZE
>         y = row_idx * TILE_SIZE
>         
>         if char == 'X':
>             Tile((x, y))
>         elif char == 'P':
>             Player((x, y))
> ```

---

## 🧠 LEARNED TODAY

* **Data-Driven Design:** Instead of putting level data in code logic, we put it in a data structure (the list). This separates "Engine" code from "Content" creation.
* **Collision Reuse:** We passed the `tile_group` into the Player class so the player knows what obstacles exist without needing global variables.

---

## 🧪 PRACTICE / EXERCISES

**Exercise: Danger Tiles**
Goal: Add Lava that resets the player.

```python
# In Tile Class
if type == 'L':
    self.image.fill((255, 100, 0)) # Orange

# In Player Update
lava_hits = pygame.sprite.spritecollide(self, lava_group, False)
if lava_hits:
    self.pos = pygame.math.Vector2(100, 200) # Reset
````

---

## 🎯 GOALS FOR TOMORROW

> [!todo] ⚔️ **Day 16: Combat & Shooting**
> 
> - Implement shooting mechanics (spawning bullet prefabs).
>     
> - Add cooldown timers (firerate).
>     
> - Handle Bullet vs Enemy collisions.


