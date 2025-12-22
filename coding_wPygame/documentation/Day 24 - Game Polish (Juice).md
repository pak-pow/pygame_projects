Tags: [[Programming]], [[Python]], [[PyGame]], [[Game]]

---
### 1) Learning Goal

You will learn to implement **High-Fidelity Game Feel** ("Juice"). This involves a **Trauma-based Screenshake** system (nonlinear decay) and **Additive Particles** that glow when they overlap.

### 2) Clear Overview

- **The Trauma System:** Instead of shaking randomly, we add "Trauma" (0.0 to 1.0) to a counter.
    
    - Trauma decays linearly (slowly returns to 0).
        
    - Shake intensity is `Trauma²`.
        
    - _Result:_ Big impacts feel massive, but the shake settles down smoothly, not abruptly.
        
- **Additive Blending:** We change how pixels combine.
    
    - Normal: `New Pixel` replaces `Old Pixel`.
        
    - Additive: `New Pixel + Old Pixel = Brighter Pixel`.
        
    - _Result:_ Explosions look like actual light/fire.
        

### 3) Deep Explanation

A. The Math of Trauma

If we just used shake = 10, it snaps on/off. It feels robotic.

If we use trauma:

1. **Hit:** `trauma = 1.0` (Max).
    
2. **Calc:** `offset = max_shake * (trauma * trauma) * random_direction`.
    
3. **Decay:** `trauma -= dt`.
    

By squaring the trauma (`t * t`), a trauma of `0.5` produces only `0.25` shake. This makes the tail end of the shake subtle and satisfying.

B. Render Offsets

We don't actually move the player or the world variables. We only move where we draw the screen.

screen.blit(world_surface, (shake_x, shake_y))

C. Hit Stop (Sleep)

To make hits feel heavy, we freeze the game for a tiny fraction of a second (e.g., 50ms) right when an impact happens.

### 4) Runnable Pygame Code Example

**Controls:**

- **Click:** Create an explosion (Trauma Shake + Glow Particles).
    
- **Right Click:** Add small trauma (Subtle shake).
    

```  Python
import pygame, sys, random

# 1. Setup
pygame.init()
SCREEN_W, SCREEN_H = 800, 600
display_surface = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()

# We draw everything to this 'wrapper' surface first, then shake THIS surface
world_surf = pygame.Surface((SCREEN_W, SCREEN_H))

# --- ADVANCED CLASSES ---

class ShakeManager:
    def __init__(self):
        self.trauma = 0.0
        self.shake_power = 20 # Max pixels to shake
        self.decay = 0.8 # How fast trauma falls per second

    def add_trauma(self, amount):
        self.trauma = min(self.trauma + amount, 1.0) # Cap at 1.0

    def update(self, dt):
        if self.trauma > 0:
            self.trauma -= self.decay * dt
            if self.trauma < 0: self.trauma = 0

    def get_offset(self):
        # The Secret Sauce: Square the trauma
        intensity = self.trauma * self.trauma
        
        dx = (random.random() * 2 - 1) * self.shake_power * intensity
        dy = (random.random() * 2 - 1) * self.shake_power * intensity
        return int(dx), int(dy)

class GlowParticle(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__()
        self.pos = pygame.math.Vector2(pos)
        self.vel = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * random.randint(100, 300)
        self.radius = random.randint(10, 25)
        self.color = color
        self.life = 1.0
        
        # Create a surface with per-pixel alpha for the glow
        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=pos)

    def update(self, dt):
        self.life -= dt
        self.pos += self.vel * dt
        self.rect.center = self.pos
        
        # Shrink
        if self.life > 0:
            scale = int(self.radius * 2 * self.life)
            if scale > 0:
                self.image = pygame.transform.scale(self.image, (scale, scale))
                self.rect = self.image.get_rect(center=self.rect.center)
        else:
            self.kill()

# --- SETUP ---
shaker = ShakeManager()
particles = pygame.sprite.Group()

while True:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Left Click: Big Boom
            if event.button == 1:
                shaker.add_trauma(1.0) # Max Trauma
                for _ in range(20):
                    particles.add(GlowParticle(event.pos, (255, 100, 50))) # Orange Fire
            
            # Right Click: Small Bump
            if event.button == 3:
                shaker.add_trauma(0.3)

    # 1. Update Logic
    shaker.update(dt)
    particles.update(dt)

    # 2. Draw World (To the temporary surface)
    world_surf.fill((30, 30, 40))
    
    # Draw Grid (to see movement easier)
    for x in range(0, 800, 50):
        pygame.draw.line(world_surf, (50, 50, 60), (x, 0), (x, 600))
    for y in range(0, 600, 50):
        pygame.draw.line(world_surf, (50, 50, 60), (0, y), (800, y))

    # Draw Particles with ADDITIVE blending (The Glow Trick)
    # We have to draw them manually to use the blend flag
    for p in particles:
        # BLEND_ADD makes colors stack and get brighter
        world_surf.blit(p.image, p.rect, special_flags=pygame.BLEND_ADD)

    # 3. Final Render (Apply Shake)
    offset = shaker.get_offset()
    display_surface.fill((0, 0, 0)) # Clean edges
    display_surface.blit(world_surf, offset)
    
    pygame.display.update()
```

### 5) 20-Minute Drill

**Task: Implement "Hit Stop" (Freeze Frame)**

1. Create a variable `hit_stop_timer = 0`.
    
2. In the loop, before `dt` is calculated:
    
    - If `hit_stop_timer > 0`: `dt = 0` (pause logic) and `hit_stop_timer -= 1`.
        
    - Else: `dt = clock.tick(60) / 1000`.
        
3. When you **Left Click**, set `hit_stop_timer = 5` (Freeze for 5 frames).
    
4. _Observe:_ The explosion feels much "crunchier" because the game momentarily halts to emphasize the impact.
    

### 6) Quick Quiz

1. **Why do we draw to `world_surf` instead of `display_surface` directly?**
    
2. **What visual difference does `BLEND_ADD` create compared to standard drawing?**
    
3. **Why do we square the trauma (`t * t`) when calculating offset?**
    

**Answers:**

1. So we can move the _entire_ image of the game by `(shake_x, shake_y)` in one blit command.
    
2. It adds pixel values together, making overlapping areas brighter (creating a glowing/light effect).
    
3. To create a non-linear falloff. It keeps high-intensity shakes violent but makes the settling phase smooth.
    

### 7) Homework for Tomorrow

**Add Polish to your RPG (Day 23)**

- **Shake:** When the Player takes damage, add `trauma=0.5`.
    
- **Flash:** When an Enemy dies, draw a white rectangle over the whole screen (`alpha=255`) and fade it out (`alpha -= 10`) over a few frames.
    

### 8) Progress to Mastery

🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜⬜⬜⬜⬜ **80%**

### 9) Obsidian Note

## 🧠 CONCEPT SUMMARY

#### The Trauma Shake Algorithm
Instead of setting a shake timer, we use a "Trauma" value (0 to 1).
> [!note] Formula
> `Shake = Max_Offset * (Trauma * Trauma)`
> `Trauma` decays linearly over time.
> Squaring it makes the shake fade out smoothly rather than abruptly.

#### Additive Blending
Normal drawing replaces pixels. Additive drawing sums them up.
* **Math:** `(100, 0, 0) + (100, 0, 0) = (200, 0, 0)`
* **Usage:** Fire, Lasers, Magic, Explosions.
* **Code:** `surface.blit(image, pos, special_flags=pygame.BLEND_ADD)`

#### Hit Stop (Sleep)
Intentionally pausing the game loop for a few milliseconds (10-50ms) when a heavy impact occurs. This gives the player's brain time to register the power of the hit.

---

## 🛠️ WHAT I DID TODAY
* **Built a Shake Manager:** Created a class to handle trauma and calculate offsets.
* **Implemented Render Offsets:** Drew the game to a temporary surface, then blitted that surface to the screen with a random offset.
* **Used Additive Blending:** Made explosion particles glow by adding their colors together.

---

## 💻 SOURCE CODE
> [!example]- TRAUMA SHAKE
> ```python
> def get_shake_offset(self):
>     intensity = self.trauma ** 2
>     dx = (random.random() * 2 - 1) * self.max_shake * intensity
>     dy = (random.random() * 2 - 1) * self.max_shake * intensity
>     return dx, dy
> ```

---

## 🎯 GOALS FOR TOMORROW
> [!todo] 🧊 **Day 25: Intro to 3D (PyOpenGL)**
> * We are breaking the 2D plane!
> * Learn to install PyOpenGL.
> * Render a rotating 3D Cube (Wireframe).
> * Understand Vertices, Edges, and Surfaces.
```