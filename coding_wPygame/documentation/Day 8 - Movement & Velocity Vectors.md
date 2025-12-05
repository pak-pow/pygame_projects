Tags: [[Programming]], [[Python]], [[PyGame]], [[Game]]

---
Welcome to **Day 8: Movement & Velocity Vectors**.

Today we will graduate from "beginner movement" (`x += 5`) to **Professional Physics**. Have you ever noticed in simple games that when you move diagonally (Up + Right), you move _faster_ than when you just move Up or Right? That is a math bug. Today, we fix it using **Vectors**.

### 1) Learning Goal

We will learn to use `pygame.math.Vector2` to handle position and velocity, and use **Normalization** to ensure diagonal movement speed is consistent.

### 2) Clear Overview

- **The Old Way:** Managing `x` and `y` variables separately.
- **The New Way:** Using a **Vector** (a single object holding both x and y).
- **The Problem:** $5 + 5 = 10$. Moving 5 pixels Up and 5 pixels Right results in a diagonal distance of ~7.07 pixels (Pythagorean theorem). That is ~40% faster!
- **The Fix:** **Normalization**. Scaling the diagonal vector back down so its total length is 5.

### 3) Deep Explanation

A. What is a Vector?

In physics and games, a Vector represents a quantity that has both Magnitude (length/speed) and Direction.

In Pygame, vec = pygame.math.Vector2(x, y) creates a vector.

- `vec.x` accesses the X component.
- `vec.y` accesses the Y component.
- **Math is easy:** `vec3 = vec1 + vec2` works automatically!

B. The Diagonal Bug

If we add 5 to X and 5 to Y per frame:

- Horizontal speed: 5
- Vertical speed: 5    
- Diagonal speed: $\sqrt{5^2 + 5^2} \approx 7.07$


![Image of vector addition triangle](https://encrypted-tbn1.gstatic.com/licensed-image?q=tbn:ANd9GcRHuuN73izi5wO7_fPvMpQCWZHesl7NHjLpUlC54CMncab7ziFlur5xSiLDADFZ2Qs9hIud_w090Lv8deoMG-CVJeg_PKW-Z0exPZRWNZmogURvIIo)


C. Normalization

To fix this, we "Normalize" the direction vector.

1. We find the direction (e.g., Left + Up = `(-1, -1)`).
2. We **Normalize** it, which keeps the direction but shrinks the length to **1**.
3. We multiply by our desired **Speed**.
    

---

### 4) Runnable Pygame Code Example

This code compares "Bad Movement" (Red Square) vs "Vector Movement" (Green Square).

Use Arrow Keys to move both. Notice how the Red one is faster on diagonals, but the Green one stays steady.

``` python
import pygame, sys

# 1. Setup
pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

# 2. Define Vectors
# We use Vector2 for position so we can use floats for precision
player_pos = pygame.math.Vector2(300, 200)
player_speed = 300 # pixels per second

# Old style player (for comparison)
bad_pos = [300, 200]

while True:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 3. Input Handling
    keys = pygame.key.get_pressed()
    
    # Create a "Direction Vector" (x, y)
    # Start at (0,0) - no movement
    input_vector = pygame.math.Vector2(0, 0)
    
    if keys[pygame.K_LEFT]:
        input_vector.x -= 1
        bad_pos[0] -= player_speed * dt
    if keys[pygame.K_RIGHT]:
        input_vector.x += 1
        bad_pos[0] += player_speed * dt
    if keys[pygame.K_UP]:
        input_vector.y -= 1
        bad_pos[1] -= player_speed * dt
    if keys[pygame.K_DOWN]:
        input_vector.y += 1
        bad_pos[1] += player_speed * dt

    # 4. Normalization Logic
    # If the vector has length (meaning keys are pressed)...
    if input_vector.length() > 0:
        # ...normalize it! This makes the length exactly 1.
        # e.g., (1, 1) becomes (0.707, 0.707)
        input_vector = input_vector.normalize()
        
        # Apply speed and delta time
        player_pos += input_vector * player_speed * dt

    # 5. Drawing
    screen.fill((0, 0, 0))
    
    # Draw Bad Player (Red) - Moves faster diagonally
    pygame.draw.rect(screen, (255, 0, 0), (round(bad_pos[0]), round(bad_pos[1]), 40, 40))
    
    # Draw Vector Player (Green) - Consistent speed
    pygame.draw.rect(screen, (0, 255, 0), (round(player_pos.x), round(player_pos.y), 40, 40))
    
    pygame.display.update()
```

## 🧠 CONCEPT SUMMARY

### **Vectors (`Vector2`)**

A mathematical object holding an X and Y component.

> [!note]  
> `pos = pygame.math.Vector2(100, 100)` replaces  
> `x = 100`  
> `y = 100`

- Stores both **direction + magnitude**    
- Perfect for movement, physics, and 2D math
- Operations like `+`, `-`, `*` just work naturally

---
### **Vector Math**

Using vectors improves code readability and precision.

> [!note]  
> `pos += velocity * dt`  
> Updates both X and Y **in a single line**.

---
### **The Diagonal Movement Bug**

When moving diagonally:

$$ \text{speed} = \sqrt{5^2 + 5^2} \approx 7.07 $$

This makes diagonal movement **~40% faster**.

---
### **Normalization**

The fix for diagonal movement speed.

> [!note]  
> `vector.normalize()` keeps direction but changes magnitude to **1**.

Example:  
`(1, 1)` → `(0.707, 0.707)`

This ensures **consistent movement speed** in all directions.

---
### **Isometric Projection**

A technique to draw 2D tiles to look like 3D (2.5D).

> [!important] **Conversion Formula**  
> **Iso X** = `(GridX - GridY) * (TileWidth / 2)`  
> **Iso Y** = `(GridX + GridY) * (TileHeight / 2)`

This turns a square grid into a **diamond** isometric map.

---

## 🛠️ **WHAT I DID TODAY**

- ✔️ Learned how to use **Vector2** for movement    
- ✔️ Fixed diagonal speed using **normalization**
- ✔️ Built a movement demo comparing:
    
    - ❌ Bad Movement (separate x/y) vs.
    - ✔️ Vector Movement (consistent speed)
        
- ✔️ Created an **Isometric Renderer** using projection math
- ✔️ Added **camera movement** using vectors
- ✔️ Refactored code to follow cleaner vector physics

---
## 💻 **SOURCE CODE**

### **Vector Movement Example**

> [!example] Clean Vector Movement Code
> 
> ```python
> import pygame
> 
> position = pygame.math.Vector2(100, 100)
> speed = 300
> 
> input_vec = pygame.math.Vector2(0, 0)
> keys = pygame.key.get_pressed()
> 
> if keys[pygame.K_LEFT]:  input_vec.x -= 1
> if keys[pygame.K_RIGHT]: input_vec.x += 1
> if keys[pygame.K_UP]:    input_vec.y -= 1
> if keys[pygame.K_DOWN]:  input_vec.y += 1
> 
> if input_vec.length() > 0:
>     input_vec = input_vec.normalize()
> 
> position += input_vec * speed * dt
> ```

---
### **Isometric Coordinate Conversion**

> [!example] Isometric Formula
> 
> ```python
> def cart_to_iso(grid_x, grid_y):
>     iso_x = (grid_x - grid_y) * (TILE_W / 2)
>     iso_y = (grid_x + grid_y) * (TILE_H / 2)
>     return pygame.math.Vector2(iso_x, iso_y)
> ```

---

### **Full Isometric Grid Renderer (Camera + Movement)**

### **📌 Overview**

This system renders an **isometric grid**, supports **camera movement**, and allows flexible tile placement.  
The renderer converts 2D coordinates → isometric screen space.

---

### **📐 Core Concept: Cartesian → Isometric**

$$  
x_{iso} = (x - y) \cdot \frac{\text{TILE WIDTH}}{2}  
$$

$$  
y_{iso} = (x + y) \cdot \frac{\text{TILE HEIGHT}}{2}  
$$

---
### **🎮 Features**

- Iso projection 
- Camera movement
- Adjustable tile scaling
- Supports layers (ground / objects)
- Smooth movement with arrow/WASD
- Modular so you can plug it into any game

---

### **🧩 Main Structure**

```python
class IsoMap:
    def __init__(self, rows, cols, tile_w, tile_h):
        self.rows = rows
        self.cols = cols
        self.tile_w = tile_w
        self.tile_h = tile_h

    def to_iso(self, x, y):
        iso_x = (x - y) * (self.tile_w // 2)
        iso_y = (x + y) * (self.tile_h // 2)
        return iso_x, iso_y

    def draw(self, surface, camera):
        for row in range(self.rows):
            for col in range(self.cols):
                iso_x, iso_y = self.to_iso(row, col)
                surface.blit(
                    tile_img, 
                    (iso_x - camera.x, iso_y - camera.y)
                )
```

---
### **🎥 Camera System**

```python
class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = 8

    def move(self, keys):
        if keys[pygame.K_w]: self.y -= self.speed
        if keys[pygame.K_s]: self.y += self.speed
        if keys[pygame.K_a]: self.x -= self.speed
        if keys[pygame.K_d]: self.x += self.speed
```

---
### **🖼 Game Loop Integration**

```python
camera = Camera()
iso_map = IsoMap(20, 20, 64, 32)

while True:
    keys = pygame.key.get_pressed()
    camera.move(keys)

    screen.fill((20, 20, 20))
    iso_map.draw(screen, camera)

    pygame.display.update()
    clock.tick(60)
```

---

## 🧠 **LEARNED TODAY**

- **Vector arithmetic** is cleaner and more powerful than separate x/y vars
- Using `normalize()` prevents unwanted fast diagonal movement
- `Vector2` integrates perfectly with **delta time** (`dt`)
- Understanding how **screen coordinates** differ from **grid coordinates**
- Isometric math = rotated + scaled 2D grid
- Camera movement becomes very easy with vectors

---

## 🧪 PRACTICE / EXERCISES

### **Exercise 1 — Refactor Player Class to Vector Movement**

```python
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ...
        self.rect = ...
        self.pos = pygame.math.Vector2(300, 300)
        self.speed = 300

    def update(self, dt):
        direction = pygame.math.Vector2(0, 0)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  direction.x -= 1
        if keys[pygame.K_RIGHT]: direction.x += 1
        if keys[pygame.K_UP]:    direction.y -= 1
        if keys[pygame.K_DOWN]:  direction.y += 1

        if direction.length() > 0:
            direction = direction.normalize()

        self.pos += direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
```

---

### **Exercise 2 — Mini Isometric Challenge**

- Render a 10×10 map
- Move the camera using arrow keys
- Change a tile's color when clicked
- (Optional) Add height for blocks

---

## 📚 **Quick Quiz**

1. **What is the length of the vector `(1, 1)`?**  
    → ~1.414
    
2. **What does `.normalize()` do?**  
    → Keeps direction, sets length = 1
    
3. **Why must we check `.length() > 0` before normalizing?**  
    → To avoid dividing by zero (normalizing 0,0 is impossible)

---
## 🎯 **GOALS FOR TOMORROW — Day 9: Platformer Physics**

> [!todo] 🍎 **Upcoming Lessons**
> 
> - Implement **gravity** as a constant downward force
>     
> - Add **jumping mechanics**
>     
> - Handle **floor collision**
>     
> - Use vectors for velocity & acceleration
>     

---

## 📈 **Progress to Mastery**

🟩🟩🟩🟩🟩🟩🟩🟩⬜⬜ **26%**

