Tags: [[Python]], [[PyGame]], [[Game]], [[Programming]]

---
Today we are gonna stop writing "Spaghetti Code" (long lists of unorganized variables) and start writing **Professional Game Code** using **Object-Oriented Programming (OOP)**.

#### 1) Learning Goal

will learn how to organize your game objects into **Classes** (Blueprints) using `pygame.sprite.Sprite` and manage them efficiently with **Sprite Groups**.

#### 2) Clear Overview

In your Pong game, you had variables like `BALL_POS_X`, `BALL_SPEED_X`, `PLAYER_POS_X`, etc. If you wanted 10 balls, you'd need 30 new variables! 😱

With **OOP**, we create a **Class** (a Blueprint).

- **Class:** `Ball` (The blueprint).
    
- **Instance:** `ball1`, `ball2`, `ball3` (Actual objects built from the blueprint).
    

Pygame provides a special parent class called **`pygame.sprite.Sprite`**. If we use it, we get powerful tools to manage updating and drawing automatically.

#### 3) Deep Explanation

**A. The Class Structure**

- A class groups Data (variables) and Behavior (functions) together.

- Functions inside a class are called Methods.

- Variables inside a class are called Attributes (and we access them using self).

**B. The init Method**

- This is the "Constructor". It runs automatically when you create a new object. We use it to set up the image and rect.

**C. The update Method**

- This is where the logic goes (movement, bouncing, inputs). We don't call this manually; the Group will call it for us!

**D. Sprite Groups**

- Instead of drawing every object manually (screen.blit(player)... screen.blit(ball)...), we put them into a Group.

- `all_sprites = pygame.sprite.Group()` 

- `all_sprites.update()`: Runs the logic for _every_ object in the group.

- `all_sprites.draw(screen)`: Draws _every_ object in the group.

---

#### 4) Runnable Pygame Code Example

This code does the exact same thing as our Day 3/4 examples (moving a player and a bouncing ball), but it is organized with **Classes**. Notice how clean the Game Loop is!


``` python
import pygame, sys
from pygame.locals import *

# 1. Setup
pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()
FPS = 60

# --- CLASSES (The Blueprints) ---

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() # Initialize parent Sprite class
        # 1. Create Image (Surface)
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 0, 255)) # Blue
        # 2. Create Rect (Position)
        self.rect = self.image.get_rect()
        self.rect.center = (300, 350)
        # 3. Physics variables (Float)
        self.pos_x = float(self.rect.x)
        self.speed = 300 # px/second

    def update(self, dt):
        # This method is run every frame automatically by the Group
        keys = pygame.key.get_pressed()
        
        if keys[K_LEFT] and self.rect.left > 0:
            self.pos_x -= self.speed * dt
        if keys[K_RIGHT] and self.rect.right < 600:
            self.pos_x += self.speed * dt
            
        # Sync Rect to Float
        self.rect.x = int(self.pos_x)

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0)) # Red
        self.rect = self.image.get_rect()
        self.rect.center = (300, 200)
        
        # Velocity
        self.velocity_x = 200
        self.velocity_y = 200
        
        # Float Position
        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y)

    def update(self, dt):
        # Move
        self.pos_x += self.velocity_x * dt
        self.pos_y += self.velocity_y * dt
        
        # Bounce Logic (Walls)
        if self.pos_x <= 0 or self.pos_x >= 570: # 600 - 30 width
            self.velocity_x *= -1
        if self.pos_y <= 0 or self.pos_y >= 370:
            self.velocity_y *= -1
            
        # Sync Rect
        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)

# --- INSTANCES (Building the Objects) ---
player = Player()
ball = Ball()

# Grouping them together
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(ball)

# --- GAME LOOP ---
while True:
    dt = clock.tick(FPS) / 1000

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # 1. UPDATE EVERYTHING
    # We pass 'dt' to update because our classes expect it!
    all_sprites.update(dt)

    # 2. DRAW EVERYTHING
    screen.fill((255, 255, 255))
    all_sprites.draw(screen) # Magic! Draws all objects in the group
    
    pygame.display.update()
```

---
#### 5) 20-Minute Drill

**Your Task:** Demonstrate the power of OOP by adding more balls.

1. Create a **second** ball instance (`ball2`) using the `Ball` class.
    
2. Start it at a different position (e.g., `ball2.pos_x = 100`).
    
3. Add it to the `all_sprites` group.
    
4. **Observation:** Notice you _didn't_ have to write any new movement logic or drawing code in the loop. It just works!
    

_Try adding 3 or 4 balls to see how easy it is now._

---

#### 6) Quick Quiz

1. *What is the name of the function inside a class that runs automatically when you create an object?*
    
2. *Why do we use `super().__init__()`?*
    
3. *If you have 50 enemies in a Group called `enemies`, what single line of code draws them all?*

**Answers:**

1. `__init__`
    
2. To make sure the parent `pygame.sprite.Sprite` class sets itself up correctly before we add our own custom data.
    
3. `enemies.draw(screen)`
    

---

#### 7) Homework 

Take your **Vertical Pong** code from Day 4 and refactor it completely to use Classes.

- Create a `Paddle` class.
    
- Create a `Ball` class.
    
- Use a Sprite Group for drawing.
    
- _Hint:_ You can pass the `player` object into the ball's update function if you need to check collisions! `ball.update(dt, player)`
    

---

#### 8) Progress to Mastery

🟩🟩🟩🟩🟩⬜⬜⬜⬜⬜ **16%**

---

#### 9) Obsidian Note


## 🧠 CONCEPT SUMMARY

#### Object Oriented Programming (OOP):
Instead of scattered variables (`ball_x`, `ball_y`, `player_x`), we wrap data and logic into **Classes**. A Class is a blueprint; an Object (Instance) is the thing we use.

#### pygame.sprite.Sprite:

The base class provided by Pygame. By inheriting from this (`class Player(pygame.sprite.Sprite)`), our objects gain compatibility with Groups.

> [!important] Requirement
> Every Sprite class **MUST** have `self.image` (Surface) and `self.rect` (Rect).

#### Sprite Groups:
A List-like container (`pygame.sprite.Group`) that holds sprites.

* **`group.update()`**: Calls the `update()` method of every sprite in the group.

* **`group.draw(screen)`**: Draws every sprite's `image` at its `rect` location.

#### Collision Belongs to the Moving Object

The **Ball** reacts when it hits the Player, so:

- Collision detection is inside `Ball.update()`    
- The Player does NOT need to know the Ball exists

---

## 🛠️ WHAT I DID TODAY

* **Created Classes:** Built a `Player` class and a `Ball` class inheriting from `Sprite`.

* **Used `__init__`:** Set up the image, rect, and physics variables inside the constructor.

* **Used `update`:** Moved the movement logic out of the main loop and into the class's `update()` method.

* **Managed Groups:** Used a `Group` to update and draw multiple objects with single commands, proving how scalable OOP is.

---

## 💻 SOURCE CODE

#### Player Class

```python
class Player(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(center=(300, 500))
        self.pos_x = float(self.rect.x)
        self.speed = 300

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if (keys[K_LEFT] or keys[K_a]) and self.rect.left > 0:
            self.pos_x -= self.speed * dt
        if (keys[K_RIGHT] or keys[K_d]) and self.rect.right < 600:
            self.pos_x += self.speed * dt

        self.rect.x = int(self.pos_x)
```

#### Ball Class

```python
class Ball(Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(center=(300, 200))

        self.vel_x = 0
        self.vel_y = 400
        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y)

        self.player = player  # Used for collision

    def update(self, dt):
        # Movement
        self.pos_x += self.vel_x * dt
        self.pos_y += self.vel_y * dt

        # Wall bounce
        if self.pos_x <= 0 or self.pos_x >= 580:
            self.vel_x *= -1
        if self.pos_y <= 0:
            self.vel_y *= -1

        # ===== COLLISION WITH PLAYER =====
        if self.rect.colliderect(self.player.rect):
            self.vel_y *= -1
            self.rect.bottom = self.player.rect.top
            self.pos_y = float(self.rect.y)

        # Sync positions
        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)

```

## 🧠 LEARNED TODAY

* **Scalability:** Adding 100 balls requires 3 lines of setup code and **zero** changes to the game loop.

* **Clean Code:** The game loop no longer contains math or logic; it just acts as a conductor (`update`, `draw`).

* **Self:** Inside a class, `self` refers to "this specific object". `self.rect.x` means "My specific X position".

---
## 🧪 PRACTICE / EXERCISES

### 1. Spawn 3 Balls

```python
for _ in range(3):
    b = Ball(player)
    b.pos_x = random.randint(0, 600)
    all_sprites.add(b)
```

### 2. Add Spin to Ball Based on Collision Offset

```python
offset = (self.rect.centerx - self.player.rect.centerx)
self.vel_x += offset * 5
```

### 3. Make Ball Faster After Every Paddle Hit

```python
self.vel_y *= 1.05
```

---

## 💡 NOTES TO SELF

> [!important] Parent Initialization:
> 
> Always call super().__init__() first inside your class's __init__ method, or the Sprite features won't work.

---
## 🎯 GOALS FOR TOMORROW

> [!todo] 💥 **Day 6: Collision Detection (Advanced)**
> 
> - Learn `pygame.sprite.spritecollide` (Group vs Sprite).
>     
> - Learn `groupcollide` (Group vs Group).
>     
> - Implement "Masks" for pixel-perfect collision (not just boxes).

---
