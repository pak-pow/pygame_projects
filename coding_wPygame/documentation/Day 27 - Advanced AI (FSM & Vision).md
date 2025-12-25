Tags: [[Programming]], [[Python]], [[PyGame]], [[Game]], [[OpenGL]]

----
### 1) Learning Goal

You will learn to implement a **Finite State Machine (FSM)** to organize complex enemy behavior and use **Vector Math (Dot Product)** to create a "Vision Cone" so enemies can only see what is in front of them.

### 2) Clear Overview

- **The Problem:** "Spaghetti Code." If you write `if dist < 50 and ammo > 0 and not sleeping or (alert and distance < 100)...`, your code becomes unreadable.
    
- **The Solution:** **States**. An enemy can only be in ONE state at a time.
    
    - **PATROL:** Walk between points A and B. Ignore player unless seen.
        
    - **CHASE:** Run toward player.
        
    - **SEARCH:** Player vanished. Go to last known spot and wait.
        
- **The Vision Cone:** Enemies shouldn't have eyes in the back of their heads. We check the angle between the _Enemy's Forward Direction_ and the _Vector to Player_.
    

### 3) Deep Explanation

A. The Finite State Machine (FSM)

An FSM is a variable (self.state) and a big if/elif block.

- `update()` calls specific functions based on the state.
    
- `patrol()` handles walking.
    
- `chase()` handles running.
    
- **Transitions:** The magic happens when we _switch_ states. E.g., `if can_see_player(): self.state = 'CHASE'`.
    

B. The Vision Cone (Dot Product)

How do we know if the enemy is facing the player?

1. Get **Vector to Player** (`V = Player - Enemy`).
    
2. Get **Enemy Forward Vector** (`F`).
    
3. **Angle Check:** `angle = V.angle_to(F)`.
    
4. If `abs(angle) < 45` (degrees), the player is inside a 90-degree cone.
    

### 4) Runnable Pygame Code Example

**Controls:**

- **WASD:** Move Player (Blue).
    
- **Enemy (Red):** Patrols automatically.
    
    - **White Lines:** Vision Cone.
        
    - **Yellow:** Alert (Heards you, but can't see you).
        
    - **Red:** Chase (Sees you).
        
``` Python
import pygame, sys, math

# 1. Setup
pygame.init()
SCREEN_W, SCREEN_H = 800, 600
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)

# --- CLASSES ---
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((0, 100, 255))
        self.rect = self.image.get_rect(center=(100, 500))
        self.pos = pygame.math.Vector2(100, 500)
        self.speed = 250

    def update(self, dt):
        keys = pygame.key.get_pressed()
        move = pygame.math.Vector2(0, 0)
        if keys[pygame.K_w]: move.y -= 1
        if keys[pygame.K_s]: move.y += 1
        if keys[pygame.K_a]: move.x -= 1
        if keys[pygame.K_d]: move.x += 1
        
        if move.length() > 0:
            self.pos += move.normalize() * self.speed * dt
            self.rect.center = round(self.pos)

class SmartEnemy(pygame.sprite.Sprite):
    def __init__(self, waypoints):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=waypoints[0])
        self.pos = pygame.math.Vector2(waypoints[0])
        
        # AI Stats
        self.waypoints = waypoints
        self.wp_index = 0
        self.speed = 100
        self.sight_range = 250
        self.sight_angle = 45 # Degrees (Total cone = 90)
        
        # State
        self.state = "PATROL"
        self.forward = pygame.math.Vector2(1, 0) # Facing Right
        self.target_pos = None

    def can_see_player(self, player):
        # 1. Distance Check
        to_player = player.pos - self.pos
        dist = to_player.length()
        if dist > self.sight_range:
            return False
            
        # 2. Angle Check (Vision Cone)
        # We need the angle between 'Forward' and 'To Player'
        angle_diff = self.forward.angle_to(to_player)
        
        # angle_to returns -180 to 180. We just care about the absolute difference.
        if abs(angle_diff) < self.sight_angle:
            return True
        return False

    def patrol(self, dt):
        # Move to current waypoint
        target = pygame.math.Vector2(self.waypoints[self.wp_index])
        direction = target - self.pos
        
        if direction.length() < 5:
            # Reached waypoint, go to next
            self.wp_index = (self.wp_index + 1) % len(self.waypoints)
        else:
            self.pos += direction.normalize() * self.speed * dt
            self.forward = direction.normalize()

    def chase(self, dt, player):
        # Move to Player
        direction = player.pos - self.pos
        self.pos += direction.normalize() * (self.speed * 1.5) * dt
        self.forward = direction.normalize()

    def update(self, dt, player):
        # --- STATE TRANSITIONS ---
        seen = self.can_see_player(player)
        
        if self.state == "PATROL":
            if seen:
                self.state = "CHASE"
        
        elif self.state == "CHASE":
            if not seen:
                self.state = "SEARCH" # Lost visual, go check last spot
                self.target_pos = player.pos # Remember where we saw them
                
        elif self.state == "SEARCH":
            if seen:
                self.state = "CHASE"
            else:
                # Walk to last known position
                direction = self.target_pos - self.pos
                if direction.length() < 5:
                    self.state = "PATROL" # Gave up
                else:
                    self.pos += direction.normalize() * self.speed * dt
                    self.forward = direction.normalize()

        # --- EXECUTE STATE ---
        if self.state == "PATROL":
            self.patrol(dt)
        elif self.state == "CHASE":
            self.chase(dt, player)
            
        self.rect.center = round(self.pos)

    def draw_debug(self, surface):
        # Draw Vision Cone Lines
        start = self.rect.center
        # Rotate forward vector by +45 and -45 degrees
        v_left = self.forward.rotate(-self.sight_angle) * self.sight_range
        v_right = self.forward.rotate(self.sight_angle) * self.sight_range
        
        pygame.draw.line(surface, (255, 255, 255), start, start + v_left, 1)
        pygame.draw.line(surface, (255, 255, 255), start, start + v_right, 1)
        pygame.draw.line(surface, (255, 255, 255), start + v_left, start + v_right, 1) # Arc cap

# --- MAIN LOOP ---
player = Player()
# Waypoints in a square shape
waypoints = [(200, 200), (600, 200), (600, 400), (200, 400)]
enemy = SmartEnemy(waypoints)

while True:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    player.update(dt)
    enemy.update(dt, player)

    screen.fill((30, 30, 30))
    
    # Draw Waypoints
    for wp in waypoints:
        pygame.draw.circle(screen, (50, 50, 50), wp, 5)

    screen.blit(player.image, player.rect)
    screen.blit(enemy.image, enemy.rect)
    enemy.draw_debug(screen)
    
    # Draw State Text
    state_surf = font.render(f"State: {enemy.state}", True, (255, 255, 0))
    screen.blit(state_surf, (enemy.rect.x, enemy.rect.y - 20))

    pygame.display.flip()
```

### 5) 20-Minute Drill

**Task: Add "Hearing" (Proximity Override)**

1. Add a `hearing_range = 100` variable to the Enemy.
    
2. Modify `can_see_player`:
    
    - Currently, it returns `False` if `angle > 45`.
        
    - **Change:** If `distance < hearing_range`, return `True` **regardless of angle**.
        
3. **Test:** Walk up _behind_ the enemy. It should notice you when you get very close (backstab prevention).
    

### 6) Quick Quiz

1. **What vector method calculates the degrees between two vectors?**
    
2. **Why do we switch to a "SEARCH" state instead of going straight back to "PATROL" when visual is lost?**
    
3. **If `forward` is `(1, 0)` (Right) and `to_player` is `(0, 1)` (Down), what is the angle?**
    

**Answers:**

1. `vector_a.angle_to(vector_b)`
    
2. To make the AI feel smarter. Real things investigate where they last saw the target; they don't instantly forget you existed.
    
3. 90 degrees.
    

### 7) Homework for Tomorrow

**Balance Your Game.**

- Take your Day 24 or 27 Code.
    
- Play it.
    
- Is the Enemy too fast? (Lower `speed`).
    
- Is the Vision Cone too wide? (Lower `sight_angle`).
    
- Create a "Config" section at the top of your script with constants like `ENEMY_SPEED = 150` so you can tweak them easily.
    

### 8) Progress to Mastery

🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜⬜ **90%**

### 9) Obsidian Note

## 🧠 CONCEPT SUMMARY

#### Finite State Machine (FSM)
A design pattern where an entity is in exactly one "State" at a time.
* **Update Logic:** `if state == 'A': do_A() elif state == 'B': do_B()`
* **Transition Logic:** Checks conditions to switch states (e.g., `if saw_player: state = 'CHASE'`).

#### The Vision Cone
To simulate eyes, we check two things:
1.  **Distance:** Are they close enough? (`vector.length()`)
2.  **Angle:** Are they in front of us? (`vector.angle_to()`)

#### Vector Angles
Pygame's `vec.angle_to(vec2)` gives the angle in degrees.
* **0°**: Directly ahead.
* **180°**: Directly behind.
* **90°**: To the side.
To make a cone, we check `abs(angle) < limit` (e.g., limit 45 gives a 90-degree cone).

---

## 🛠️ WHAT I DID TODAY
* **Built an FSM:** Created an Enemy class that switches between Patrol, Chase, and Search.
* **Implemented Vision:** Used vector math to limit the enemy's detection to a specific field of view.
* **Added Debug Visuals:** Drew lines representing the vision cone to verify the math worked.

---

## 💻 SOURCE CODE
> [!example]- VISION CHECK
> ```python
> def can_see(self, target):
>     to_target = target.pos - self.pos
>     # 1. Distance
>     if to_target.length() > self.sight_dist: return False
>     # 2. Angle
>     angle = self.facing_vec.angle_to(to_target)
>     if abs(angle) < self.field_of_view: return True
>     return False
> ```

---

## 🎯 GOALS FOR TOMORROW
> [!todo] ⚖️ **Day 28: Game Balancing & Bugfixing**
> * Learn the art of "Tweakables".
> * Externalize constants so you can balance the game without rewriting code.
> * Common Bug Patterns in Pygame (and how to squash them).

---
# SOURCE CODE

```python
import pygame  
import math  
from pygame.locals import *  
from OpenGL.GL import *  
from OpenGL.GLU import *  
  
# ============ INITIALIZATION ============  
pygame.init()  
display = (1200, 800)  
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)  
pygame.display.set_caption("3D Platformer w/ Advance Ai")  
clock = pygame.time.Clock()  
pygame.event.set_grab(True)  # Grab mouse  
pygame.mouse.set_visible(False)  # Hide mouse  
  
# Camera Setup  
glMatrixMode(GL_PROJECTION)  
glLoadIdentity()  
gluPerspective(45, (display[0] / display[1]), 0.1, 500.0)  
glMatrixMode(GL_MODELVIEW)  
glEnable(GL_DEPTH_TEST)  
glEnable(GL_POLYGON_OFFSET_FILL)  
glPolygonOffset(1.0, 1.0)  
glClearColor(0.1, 0.1, 0.15, 1)  
  
  
# ============ PLAYER STATE ============  
class Player:  
    def __init__(self):  
        self.pos = [0, 2, 0]  
        self.vel = [0, 0, 0]  
        self.on_ground = False  
        self.jump_force = 0.5  
        self.gravity = 0.015  
        self.size = 0.2  
        self.yaw = 0  # Horizontal rotation  
        self.pitch = 0  # Vertical rotation  
  
    def update(self, keys, platforms, walls, mouse_delta):  
        # Handle mouse camera movement (lower sensitivity)  
        self.yaw += mouse_delta[0] * 0.2  
        self.pitch += mouse_delta[1] * 0.2  
        self.pitch = max(-89, min(89, self.pitch))  # Clamp pitch  
  
        # Movement with WASD (relative to camera direction)        rad = math.radians(self.yaw)  
        if keys[K_w]:  
            self.vel[0] += math.sin(rad) * 0.15  
            self.vel[2] -= math.cos(rad) * 0.15  
        if keys[K_s]:  
            self.vel[0] -= math.sin(rad) * 0.15  
            self.vel[2] += math.cos(rad) * 0.15  
        if keys[K_a]:  
            self.vel[0] -= math.cos(rad) * 0.15  
            self.vel[2] -= math.sin(rad) * 0.15  
        if keys[K_d]:  
            self.vel[0] += math.cos(rad) * 0.15  
            self.vel[2] += math.sin(rad) * 0.15  
  
        # Jump  
        if keys[K_SPACE] and self.on_ground:  
            self.vel[1] = self.jump_force  
            self.on_ground = False  
  
        # Gravity & Friction  
        self.vel[1] -= self.gravity  
        self.vel[0] *= 0.90  
        self.vel[2] *= 0.90  
  
        # Position  
        self.pos[0] += self.vel[0]  
        self.pos[1] += self.vel[1]  
        self.pos[2] += self.vel[2]  
  
        # Collision with platforms  
        self.on_ground = False  
        for platform in platforms:  
            if platform.check_collision(self):  
                self.on_ground = True  
  
        # Collision with walls  
        for wall in walls:  
            wall.check_collision(self)  
  
        # Fall detection - respawn  
        if self.pos[1] < -20:  
            self.pos = [0, 2, 0]  
            self.vel = [0, 0, 0]  
  
    def draw(self):  
        glPushMatrix()  
        glTranslatef(self.pos[0], self.pos[1], self.pos[2])  
        draw_cube((0.2, 0.8, 1), self.size, self.size, self.size)  
        glPopMatrix()  
  
  
# ============ WALL CLASS ============  
class Wall:  
    def __init__(self, x, y, z, sx=0.5, sy=3, sz=20, color=(0.5, 0.5, 0.5)):  
        self.pos = [x, y, z]  
        self.size = [sx, sy, sz]  
        self.color = color  
  
    def check_collision(self, player):  
        px, py, pz = player.pos  
        ps = player.size  
        sx, sy, sz = self.size  
        px_min, px_max = self.pos[0] - sx, self.pos[0] + sx  
        py_min, py_max = self.pos[1] - sy, self.pos[1] + sy  
        pz_min, pz_max = self.pos[2] - sz, self.pos[2] + sz  
  
        # Check collision with larger buffer zone  
        buffer = ps + 0.2  
        if (px_min - buffer < px < px_max + buffer and pz_min - buffer < pz < pz_max + buffer and  
                py_min - buffer < py < py_max + buffer):  
            # Calculate distances to each face  
            dx_left = abs(px - (px_min - buffer))  
            dx_right = abs((px_max + buffer) - px)  
            dz_front = abs(pz - (pz_min - buffer))  
            dz_back = abs((pz_max + buffer) - pz)  
            dy_bottom = abs(py - (py_min - buffer))  
            dy_top = abs((py_max + buffer) - py)  
  
            min_dist = min(dx_left, dx_right, dz_front, dz_back, dy_bottom, dy_top)  
  
            # Push player out of wall  
            if min_dist == dx_left:  
                player.pos[0] = px_min - ps - 0.3  
                player.vel[0] *= 0.5  
            elif min_dist == dx_right:  
                player.pos[0] = px_max + ps + 0.3  
                player.vel[0] *= 0.5  
            elif min_dist == dz_front:  
                player.pos[2] = pz_min - ps - 0.3  
                player.vel[2] *= 0.5  
            elif min_dist == dz_back:  
                player.pos[2] = pz_max + ps + 0.3  
                player.vel[2] *= 0.5  
  
    def draw(self):  
        glPushMatrix()  
        glTranslatef(self.pos[0], self.pos[1], self.pos[2])  
        draw_cube(self.color, self.size[0], self.size[1], self.size[2], filled=True)  
        glPopMatrix()  
  
  
# ============ PLATFORM CLASS ============  
class Platform:  
    def __init__(self, x, y, z, sx=2, sy=0.5, sz=4, color=(0.3, 0.5, 0.8)):  
        self.pos = [x, y, z]  
        self.size = [sx, sy, sz]  
        self.color = color  
  
    def check_collision(self, player):  
        px, py, pz = player.pos  
        ps = player.size  
        sx, sy, sz = self.size  
        px_min, px_max = self.pos[0] - sx, self.pos[0] + sx  
        py_min, py_max = self.pos[1] - sy, self.pos[1] + sy  
        pz_min, pz_max = self.pos[2] - sz, self.pos[2] + sz  
  
        if (px_min < px < px_max and pz_min < pz < pz_max and  
                py - ps < py_max and py + ps > py_min):  
            if player.vel[1] <= 0:  
                player.pos[1] = py_max + ps  
                player.vel[1] = 0  
                return True  
        return False  
    def draw(self):  
        glPushMatrix()  
        glTranslatef(self.pos[0], self.pos[1], self.pos[2])  
        draw_cube(self.color, self.size[0], self.size[1], self.size[2], filled=True)  
        glPopMatrix()  
  
  
# ============ ENEMY CLASS ============  
class Enemy:  
    def __init__(self, x, y, z, waypoint1=None, waypoint2=None):  
        self.pos = [x, y, z]  
        self.state = "PATROL"  
        self.patrol_target = [x + 20, y, z]  
        self.speed = 0.02  
        self.detect_range = 30  
        self.lost_timer = 0  
  
    def update(self, player):  
        dx = player.pos[0] - self.pos[0]  
        dz = player.pos[2] - self.pos[2]  
        dist = math.sqrt(dx * dx + dz * dz)  
  
        # State transitions  
        if dist < self.detect_range:  
            self.state = "CHASE"  
            self.lost_timer = 0  
        elif self.state == "CHASE":  
            self.lost_timer += 1  
            if self.lost_timer > 120:  
                self.state = "PATROL"  
  
        # Execute state  
        if self.state == "CHASE":  
            move_dir_x = dx / (dist + 0.1)  
            move_dir_z = dz / (dist + 0.1)  
            self.pos[0] += move_dir_x * self.speed * 1.5  
            self.pos[2] += move_dir_z * self.speed * 1.5  
        else:  
            p_dx = self.patrol_target[0] - self.pos[0]  
            p_dz = self.patrol_target[2] - self.pos[2]  
            p_dist = math.sqrt(p_dx * p_dx + p_dz * p_dz)  
  
            move_dir_x = p_dx / (p_dist + 0.1)  
            move_dir_z = p_dz / (p_dist + 0.1)  
            self.pos[0] += move_dir_x * self.speed  
            self.pos[2] += move_dir_z * self.speed  
  
            if p_dist < 1:  
                self.patrol_target[0] *= -1  
  
    def draw(self):  
        color = (1, 0.2, 0.2) if self.state == "CHASE" else (0.8, 0.6, 0.2)  
        glPushMatrix()  
        glTranslatef(self.pos[0], self.pos[1], self.pos[2])  
        draw_cube(color, 0.6, 0.8, 0.6)  
        glPopMatrix()  
  
  
# ============ DRAWING FUNCTIONS ============  
vertices = (  
    (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),  
    (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1)  
)  
edges = ((0, 1), (0, 3), (0, 4), (2, 1), (2, 3), (2, 7), (6, 3), (6, 4), (6, 7), (5, 1), (5, 4), (5, 7))  
  
  
def draw_cube(color, sx=1, sy=1, sz=1, filled=False):  
    glPushMatrix()  
    glScalef(sx, sy, sz)  
  
    if filled:  
  
        # Draw solid cube with faces  
        glColor3fv(color)  
        glBegin(GL_QUADS)  
  
        # Front face  
        glVertex3f(-1, -1, 1)  
        glVertex3f(1, -1, 1)  
        glVertex3f(1, 1, 1)  
        glVertex3f(-1, 1, 1)  
  
        # Back face  
        glVertex3f(-1, -1, -1)  
        glVertex3f(-1, 1, -1)  
        glVertex3f(1, 1, -1)  
        glVertex3f(1, -1, -1)  
  
        # Top face  
        glVertex3f(-1, 1, -1)  
        glVertex3f(-1, 1, 1)  
        glVertex3f(1, 1, 1)  
        glVertex3f(1, 1, -1)  
  
        # Bottom face  
        glVertex3f(-1, -1, -1)  
        glVertex3f(1, -1, -1)  
        glVertex3f(1, -1, 1)  
        glVertex3f(-1, -1, 1)  
  
        # Right face  
        glVertex3f(1, -1, -1)  
        glVertex3f(1, 1, -1)  
        glVertex3f(1, 1, 1)  
        glVertex3f(1, -1, 1)  
  
        # Left face  
        glVertex3f(-1, -1, -1)  
        glVertex3f(-1, -1, 1)  
        glVertex3f(-1, 1, 1)  
        glVertex3f(-1, 1, -1)  
        glEnd()  
  
        # Draw black outline  
        glColor3f(0, 0, 0)  
        glBegin(GL_LINES)  
        for edge in edges:  
            for v in edge:  
                glVertex3fv(vertices[v])  
        glEnd()  
    else:  
        # Draw wireframe cube  
        glColor3fv(color)  
        glBegin(GL_LINES)  
        for edge in edges:  
            for v in edge:  
                glVertex3fv(vertices[v])  
        glEnd()  
  
    glPopMatrix()  
  
  
def draw_grid():  
    glBegin(GL_LINES)  
    glColor3f(0.3, 0.3, 0.3)  
    for i in range(-20, 20):  
        glVertex3f(i, -1, -20)  
        glVertex3f(i, -1, 20)  
        glVertex3f(-20, -1, i)  
        glVertex3f(20, -1, i)  
    glEnd()  
  
  
# ============ SETUP LEVEL ============  
platforms = [  
    Platform(0, 0, 0, 15, 1, 15, (0.2, 0.6, 0.3)),  # Starting platform  
    Platform(0, 3, -40, 15, 1, 15, (0.2, 0.6, 0.3)),  # Middle  
    Platform(35, 6, -30, 12, 1, 12, (0.2, 0.6, 0.3)),  # Right  
    Platform(-35, 6, -30, 12, 1, 12, (0.2, 0.6, 0.3)),  # Left  
    Platform(0, 10, -80, 20, 1, 20, (0.2, 0.6, 0.3)),  # End platform  
    Platform(0, -1, 0, 200, 0.5, 200, (0.15, 0.15, 0.2)),  # Floor - solid dark color  
]  
  
player = Player()  
enemies = [  
    Enemy(30, 1, 0, [10, 1, -15], [50, 1, 15]),  
    Enemy(-30, 1, 0, [-50, 1, 15], [-10, 1, -15]),  
]  
  
# Boundary walls (keep player from going out of bounds)  
walls = [  
    Wall(80, 5, 0, 0.5, 10, 160),  # Right wall  
    Wall(-80, 5, 0, 0.5, 10, 160),  # Left wall  
    Wall(0, 5, 80, 160, 10, 0.5),  # Front wall  
    Wall(0, 5, -160, 160, 10, 0.5),  # Back wall  
]  
  
# ============ MAIN LOOP ============  
running = True  
while running:  
    dt = clock.tick(60)  
  
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            running = False  
  
    keys = pygame.key.get_pressed()  
    if keys[K_ESCAPE]:  
        running = False  
  
    # Get mouse movement  
    mouse_delta = pygame.mouse.get_rel()  
  
    # Update  
    player.update(keys, platforms, walls, mouse_delta)  
    for enemy in enemies:  
        enemy.update(player)  
  
    # Render  
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  
    glLoadIdentity()  
  
    # Camera: first-person view centered on player  
    glRotatef(player.pitch, 1, 0, 0)  
    glRotatef(player.yaw, 0, 1, 0)  
    glTranslatef(-player.pos[0], -player.pos[1], -player.pos[2])  
  
    draw_grid()  
    for platform in platforms:  
        platform.draw()  
    for wall in walls:  
        wall.draw()  
    player.draw()  
    for enemy in enemies:  
        enemy.draw()  
  
    pygame.display.flip()  
  
pygame.quit()

```
# Explanation
## **INITIALIZATION (Lines 1-24)**

```python
import pygame, math
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
```

Imports the libraries we need: pygame for the window, math for calculations, and OpenGL for 3D rendering.

```python
pygame.init()
display = (1200, 800)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
```

Creates a 1200x800 window. `DOUBLEBUF` uses double buffering (smoother rendering), `OPENGL` enables 3D graphics.

```python
pygame.event.set_grab(True)  # Grab mouse
pygame.mouse.set_visible(False)  # Hide mouse
```

Locks the mouse to the window and hides the cursor for immersive FPS controls.

```python
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, (display[0] / display[1]), 0.1, 500.0)
glMatrixMode(GL_MODELVIEW)
```

Sets up the camera: 45° field of view, aspect ratio based on window size, near plane at 0.1, far plane at 500 (anything beyond 500 units isn't rendered).

```python
glEnable(GL_DEPTH_TEST)
glEnable(GL_POLYGON_OFFSET_FILL)
glPolygonOffset(1.0, 1.0)
glClearColor(0.1, 0.1, 0.15, 1)
```

- `GL_DEPTH_TEST`: Closer objects appear in front of far objects
- `GL_POLYGON_OFFSET_FILL`: Prevents flickering when drawing outlines over solid faces
- `glClearColor`: Sets background to dark blue-gray

---

## **PLAYER CLASS (Lines 28-81)**

```python
class Player:
    def __init__(self):
        self.pos = [0, 2, 0]  # X, Y, Z coordinates
        self.vel = [0, 0, 0]  # Velocity in each direction
        self.on_ground = False
        self.jump_force = 0.5
        self.gravity = 0.015
        self.size = 0.2  # Player is a small cube
        self.yaw = 0  # Horizontal rotation (left/right)
        self.pitch = 0  # Vertical rotation (up/down)
```

Initializes the player at position (0, 2, 0), with no movement, and camera angles at 0.

```python
def update(self, keys, platforms, walls, mouse_delta):
    self.yaw += mouse_delta[0] * 0.2
    self.pitch += mouse_delta[1] * 0.2
    self.pitch = max(-89, min(89, self.pitch))
```

**Mouse Look:**

- `mouse_delta[0]` = left/right mouse movement → rotates yaw
- `mouse_delta[1]` = up/down mouse movement → rotates pitch
- `* 0.2` is sensitivity (lower = less sensitive)
- Pitch is clamped between -89° and 89° so you can't flip upside down

```python
rad = math.radians(self.yaw)
if keys[K_w]:
    self.vel[0] += math.sin(rad) * 0.08
    self.vel[2] -= math.cos(rad) * 0.08
```

**Forward Movement:**

- `rad = math.radians(self.yaw)`: Convert yaw angle to radians
- `math.sin(rad)` and `math.cos(rad)` calculate the direction you're facing
- Add velocity in that direction (0.08 is speed)
- This makes WASD movement relative to camera direction

```python
if keys[K_SPACE] and self.on_ground:
    self.vel[1] = self.jump_force
    self.on_ground = False
```

**Jump:** Only jump if touching ground. Set upward velocity to 0.5.

```python
self.vel[1] -= self.gravity
self.vel[0] *= 0.90
self.vel[2] *= 0.90
```

**Physics:**

- Gravity pulls you down (subtract 0.015 each frame)
- Friction slows horizontal movement (multiply by 0.90 = 10% slowdown per frame)

```python
self.pos[0] += self.vel[0]
self.pos[1] += self.vel[1]
self.pos[2] += self.vel[2]
```

**Apply Velocity:** Update position based on velocity.

```python
self.on_ground = False
for platform in platforms:
    if platform.check_collision(self):
        self.on_ground = True

for wall in walls:
    wall.check_collision(self)
```

**Collision:** Check if touching any platforms or walls. Platforms set `on_ground = True`.

```python
if self.pos[1] < -20:
    self.pos = [0, 2, 0]
    self.vel = [0, 0, 0]
```

**Respawn:** If you fall too far down, reset to start.

---

## **WALL CLASS (Lines 84-131)**

```python
class Wall:
    def __init__(self, x, y, z, sx=0.5, sy=3, sz=20, color=(0.5, 0.5, 0.5)):
        self.pos = [x, y, z]
        self.size = [sx, sy, sz]
        self.color = color
```

Creates a wall at position (x,y,z) with size (sx, sy, sz). Default is a thin wall (0.5 width) and gray color.

```python
def check_collision(self, player):
    px, py, pz = player.pos
    ps = player.size
    sx, sy, sz = self.size
    px_min, px_max = self.pos[0] - sx, self.pos[0] + sx
```

**Collision Setup:** Get player and wall bounds (min/max for each axis).

```python
buffer = ps + 0.2
if (px_min - buffer < px < px_max + buffer and ...):
```

**Collision Detection:** Check if player is inside wall with a buffer zone (ps = player size + 0.2 extra units). This prevents clipping through.

```python
dx_left = abs(px - (px_min - buffer))
dx_right = abs((px_max + buffer) - px)
...
min_dist = min(dx_left, dx_right, dz_front, dz_back, dy_bottom, dy_top)
```

**Find Closest Face:** Calculate distance to each wall face, find the closest one.

```python
if min_dist == dx_left:
    player.pos[0] = px_min - ps - 0.3
    player.vel[0] *= 0.5
```

**Push Out:** If hitting the left face, move player to the left of the wall and slow them down (0.5x velocity).

---

## **PLATFORM CLASS (Lines 134-159)**

Similar to Wall but checks collision differently - **only from above**:

```python
if (px_min < px < px_max and pz_min < pz < pz_max and
        py - ps < py_max and py + ps > py_min):
    if player.vel[1] <= 0:  # Only if falling down
        player.pos[1] = py_max + ps
        player.vel[1] = 0
        return True
```

**Landing:** If player is above platform and falling, snap them to the top and set vertical velocity to 0. This is how you "land" on platforms.

---

## **ENEMY CLASS (Lines 162-206)**

```python
class Enemy:
    def __init__(self, x, y, z, waypoint1=None, waypoint2=None):
        self.pos = [x, y, z]
        self.state = "PATROL"
        self.patrol_target = [x + 20, y, z]
        self.speed = 0.02
        self.detect_range = 30
        self.lost_timer = 0
```

Creates an enemy. `state = "PATROL"` means it starts patrolling. `detect_range = 30` means it sees you if you're within 30 units. **NOTE:** Your file doesn't have the advanced FSM - it has the old simple version!

```python
dx = player.pos[0] - self.pos[0]
dz = player.pos[2] - self.pos[2]
dist = math.sqrt(dx * dx + dz * dz)
```

**Calculate Distance:** Get vector from enemy to player, calculate distance.

```python
if dist < self.detect_range:
    self.state = "CHASE"
    self.lost_timer = 0
elif self.state == "CHASE":
    self.lost_timer += 1
    if self.lost_timer > 120:
        self.state = "PATROL"
```

**State Machine:**

- If player is close, switch to CHASE
- If chasing but lost player for 120 frames, switch back to PATROL

```python
if self.state == "CHASE":
    move_dir_x = dx / (dist + 0.1)
    move_dir_z = dz / (dist + 0.1)
    self.pos[0] += move_dir_x * self.speed * 1.5
```

**Chase:** Normalize direction vector and move toward player at 1.5x speed.

```python
else:
    p_dx = self.patrol_target[0] - self.pos[0]
    ...
    if p_dist < 1:
        self.patrol_target[0] *= -1
```

**Patrol:** Walk toward patrol target. When reached (distance < 1), flip to opposite side (multiply by -1).

---

## **DRAWING FUNCTIONS (Lines 209-310)**

```python
def draw_cube(color, sx=1, sy=1, sz=1, filled=False):
    glPushMatrix()  # Save current transformation
    glScalef(sx, sy, sz)  # Scale the cube
    
    if filled:
        glColor3fv(color)
        glBegin(GL_QUADS)
        # Draw 6 faces of the cube
        glVertex3f(-1, -1, 1)  # Front-bottom-left corner
        ...
```

**Solid Cube:** `GL_QUADS` draws squares. Each face = 4 vertices. 6 faces = solid cube.

```python
glColor3f(0, 0, 0)
glBegin(GL_LINES)
for edge in edges:
    for v in edge:
        glVertex3fv(vertices[v])
glEnd()
```

**Outline:** Draw black lines connecting vertices along edges.

```python
else:
    glColor3fv(color)
    glBegin(GL_LINES)
    # Wireframe version
```

If `filled=False`, only draw wireframe (just the edges).

```python
glPopMatrix()  # Restore previous transformation
```

Undo the scale so it doesn't affect other objects.

```python
def draw_grid():
    glBegin(GL_LINES)
    glColor3f(0.3, 0.3, 0.3)
    for i in range(-20, 20):
        glVertex3f(i, -1, -20)  # Horizontal lines
        glVertex3f(i, -1, 20)
```

**Grid:** Draws ground grid for reference (dark gray lines at y=-1).

---

## **MAIN LOOP (Lines 336-367)**

```python
running = True
while running:
    dt = clock.tick(60)  # 60 FPS cap
```

Loop 60 times per second.

```python
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
```

Check if user closes window.

```python
keys = pygame.key.get_pressed()
mouse_delta = pygame.mouse.get_rel()
```

Get current pressed keys and mouse movement.

```python
player.update(keys, platforms, walls, mouse_delta)
for enemy in enemies:
    enemy.update(player)
```

**Update:** Run physics and AI logic.

```python
glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
glLoadIdentity()
```

Clear the screen and reset camera.

```python
glRotatef(player.pitch, 1, 0, 0)  # Rotate around X-axis (look up/down)
glRotatef(player.yaw, 0, 1, 0)    # Rotate around Y-axis (look left/right)
glTranslatef(-player.pos[0], -player.pos[1], -player.pos[2])
```

**Camera:** Apply camera rotation and position. Negative values because camera moves opposite to player.

```python
draw_grid()
for platform in platforms:
    platform.draw()
for wall in walls:
    wall.draw()
player.draw()
for enemy in enemies:
    enemy.draw()
```

**Draw Everything:** Grid, platforms, walls, player, enemies.

```python
pygame.display.flip()
```

Show the rendered frame on screen.

```python
pygame.quit()
```

Clean up when loop ends.
