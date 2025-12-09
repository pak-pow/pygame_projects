Tags: [[Programming]], [[Python]], [[PyGame]], [[Game]] 

---
We have a game with movement, physics, and cameras. But does it feel good? Does it pop?

Today, we add Particles. These are the sparks, smoke, blood, and dust that make a game feel alive. This concept is often called "Game Juice."

### 1) Learning Goal

You will learn to create a **Particle System**: a manager that spawns hundreds of temporary objects, animates them (fading/shrinking), and deletes them automatically to save memory.

### 2) Clear Overview

- **What is a Particle?** A simple sprite that exists for a short time (e.g., 0.5 seconds) and then dies.
    
- **Fire-and-Forget:** You spawn them, they do their thing (move, shrink, change color), and then they `kill()` themselves.
    
- **The Manager:** We usually spawn them in **lists** or **groups**. For an explosion, we spawn 20-50 at once moving in random directions.
    

### 3) Deep Explanation

**A. The Lifecycle of a Particle**

1. **Birth:** Created at a specific point (e.g., where a bullet hits a wall). Given a random velocity.
    
2. **Life:** Every frame, it moves. It also changes properties (gets smaller, fades out, changes color).
    
3. **Death:** It has a `lifetime` variable. When `lifetime <= 0`, we remove it from the Group. **Crucial:** If you don't delete them, your game will lag after a few minutes because you'll have 50,000 invisible particles!

**B. Randomness**

Particles need Randomness to look natural.

- `random.uniform(-1, 1)` for direction.
- `random.randint(2, 5)` for size.

**C. Math (Circle Bursts)**

To make a circular explosion, we use trigonometry or random vectors.

vec = pygame.math.Vector2(1, 0).rotate(random.randint(0, 360)) gives a random direction.

---

### 4) Runnable Pygame Code Example

This code turns your mouse into a magic wand.

- **Left Click:** Creates a "Pop" explosion.
    
- **Hold Right Click:** Creates a continuous "Stream" (like a flamethrower).


```Python
import pygame, sys, random

# 1. Setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
pygame.display.set_caption("Day 12: Particle Effects")

# --- PARTICLE CLASS ---
class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__()
        # Randomize Size (between 4 and 10 pixels)
        self.size = random.randint(4, 10) 
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)
        
        # Physics (Position needs to be float)
        self.pos = pygame.math.Vector2(pos)
        
        # Random Velocity: Random direction, random speed
        # random.uniform gives float numbers (e.g., -2.5)
        self.vel = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.vel = self.vel.normalize() * random.randint(50, 200) # Speed
        
        # Lifetime (How many seconds to live)
        self.lifetime = random.uniform(0.2, 0.6) 

    def update(self, dt):
        # 1. Move
        self.pos += self.vel * dt
        self.rect.center = round(self.pos)
        
        # 2. Reduce Lifetime
        self.lifetime -= dt
        
        # 3. Death Check
        if self.lifetime <= 0:
            self.kill() # Removes self from ALL groups
            
        # 4. Visual "Juice" (Shrink effect)
        # Calculate new size based on remaining life
        # (This is a simplified shrink; we recreate the surface)
        if self.size > 0:
            self.size -= 10 * dt # Shrink speed
            if self.size < 1: self.size = 0 # Prevent negative size error
            
            # Re-draw the shrinking square
            self.image = pygame.Surface((int(self.size), int(self.size)))
            self.image.fill((255, 255, 255)) # Flash White as they die

# Groups
particle_group = pygame.sprite.Group()

while True:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        # EXPLOSION (Click)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i in range(30): # Spawn 30 particles at once
                p = Particle(event.pos, (255, 50, 50)) # Red
                particle_group.add(p)

    # STREAM (Hold Right Click)
    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[2]: # Right click is index 2
        pos = pygame.mouse.get_pos()
        for i in range(2): # Spawn 2 per frame
            p = Particle(pos, (50, 200, 255)) # Blue
            particle_group.add(p)

    # Update
    particle_group.update(dt)

    # Draw
    screen.fill((30, 30, 30))
    particle_group.draw(screen)
    
    # UI Info
    count_text = pygame.font.SysFont(None, 30).render(f"Particles: {len(particle_group)}", True, (255, 255, 255))
    screen.blit(count_text, (10, 10))

    pygame.display.update()
```

---

### 5) 20-Minute Drill

**Your Task:** Turn this into a **Fountain**.

1. **Gravity:** In the `Particle` update method, add Gravity (`self.vel.y += 500 * dt`).
    
2. **Direction:** In `__init__`, force the Y velocity to be **Negative** (Upwards) initially, so they shoot up and fall down.
    
3. **Color:** Make the particles **Yellow**.
    
4. **Result:** It should look like a golden fountain when you hold the mouse.
    

_This teaches you that Particles are just mini-physics objects!_

---

### 6) Quick Quiz

1. **Why do we call `self.kill()` when `lifetime <= 0`?**
    
2. **If we spawn 10 particles per frame at 60 FPS, how many particles are created in 1 second?**
    
3. **What happens if we forget to multiply the movement by `dt`?**
    

**Answers:**

1. To free up memory. If we don't, the computer will eventually crash or lag from processing thousands of invisible objects.
    
2. 600 particles.
    
3. The particles will move at different speeds on different computers (Lag = Teleporting particles).
    

---

### 7) Homework for Tomorrow

**Polish your Pong Game.**

- Add a particle system.
    
- When the ball hits the paddle, spawn 10 small white particles at the collision point (sparks).
    
- When the ball hits the wall, spawn 10 particles.
    
- _Hint:_ You pass the `BALL_OBJ.center` as the spawn position.
    

---

### 8) Progress to Mastery

🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩 **40%**

---

### 9) Obsidian Note

## 🧠 CONCEPT SUMMARY

#### What are Particles?
Temporary visual objects used to create effects like smoke, fire, explosions, and blood. They are purely visual and usually do not interact with the game world (no complex collisions).

#### The Fire-and-Forget Pattern:
1.  **Spawn:** Create the particle with random stats (speed, angle, size).
2.  **Animate:** Move and change properties (shrink/fade) every frame.
3.  **Kill:** Delete the particle when its lifetime expires.

#### The `kill()` method:
A built-in method of `pygame.sprite.Sprite`. It removes the sprite from **all** Groups it belongs to. This is essential for memory management.

---

## 🛠️ WHAT I DID TODAY

* **Created a Particle Class:** Built a sprite that handles its own movement and death.
* **Implemented Randomness:** Used `random.uniform` to create varied velocities so explosions look natural, not perfect circles.
* **Managed Lifetime:** Used a timer (`lifetime -= dt`) to automatically delete particles.
* **Added Visual Polish:** Made particles shrink over time to simulate fading away.

---

## 💻 SOURCE CODE

> [!example]- PARTICLE CLASS
> ```python
> class Particle(pygame.sprite.Sprite):
>     def __init__(self, pos):
>         super().__init__()
>         self.image = pygame.Surface((10, 10))
>         self.image.fill((255, 255, 0))
>         self.rect = self.image.get_rect(center=pos)
>         
>         # Random Direction
>         self.vel = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
>         self.vel = self.vel.normalize() * random.randint(100, 300)
>         self.lifetime = 0.5
> 
>     def update(self, dt):
>         self.lifetime -= dt
>         if self.lifetime <= 0:
>             self.kill() # Delete self
>             
>         self.rect.center += self.vel * dt
> ```

---

## 🧠 LEARNED TODAY

* **Juice:** Adding simple effects like particles drastically changes the "feel" of a game.
* **Batch Spawning:** To make an explosion, we use a `for` loop to spawn multiple particles (e.g., 30) in a single frame.
* **Performance:** Thousands of particles can slow down Python. Keep lifetimes short (0.5s - 1.0s) to keep the count low.

---

## 🧪 PRACTICE / EXERCISES

**Exercise: Gravity Fountain**
Goal: Make particles shoot up and fall down.

```python
# In __init__
# Force Upward velocity
self.vel.y = random.uniform(-300, -500) 

# In update
# Add Gravity
self.vel.y += 1000 * dt 
self.pos += self.vel * dt
````

---

## 🎯 GOALS FOR TOMORROW

> [!todo] 🔊 **Day 13: Audio (SFX & Music)**
> 
> - Learn the difference between `pygame.mixer.Sound` and `pygame.mixer.music`.
>     
> - Trigger sound effects on events (Jump, Shoot).
>     
> - Loop background music.

