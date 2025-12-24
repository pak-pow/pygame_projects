Tags: [[Programming]], [[Python]], [[PyGame]], [[Game]], [[OpenGL]]

---
### 1) Learning Goal

Implement a First-Person Camera using the **Matrix Stack** and correct **OpenGL Matrix Modes** to ensure objects render at the correct depth.
### 2) Clear Overview

- **The Fix:** We must switch to `GL_PROJECTION` to set the lens (FOV), then switch back to `GL_MODELVIEW` to draw the world.
- **The Movement:** We modify `cam_x/y/z` variables based on input.
- **The Rendering:** We translate the _World_ by `-cam_pos` to simulate the Camera moving forward.

### 3) Deep Explanation

**A. The Two Matrices**

- `GL_PROJECTION`: The Camera Lens. We set this **once** at the start. It defines FOV and Aspect Ratio.
- `GL_MODELVIEW`: The World. We update this **every frame** to move objects and the "camera" position.  

**B. glLoadIdentity()**

This command resets the current matrix to "Zero" (Identity). We must call this before moving the camera every frame, or else we will fly off into space exponentially.

### 4) Runnable Pygame Code Example

**Controls:**

- **Arrow Keys:** Move Forward/Back/Left/Right.
- **Space/Shift:** Up/Down.
- **Q/E:** Rotate Head.

``` Python
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# 1. Setup
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
clock = pygame.time.Clock()

# --- CAMERA SETUP (The Fix) ---
glMatrixMode(GL_PROJECTION) # Switch to "Lens" mode
glLoadIdentity()            # Reset lens
# FOV=45, Aspect Ratio, Near=0.1, Far=50.0
gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

glMatrixMode(GL_MODELVIEW)  # Switch back to "World" mode
glLoadIdentity()            # Reset world

# Camera Variables
cam_x, cam_y, cam_z = 0, 0, -5
cam_yaw = 0 

# Cube Data
vertices = (
    (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
    (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1)
)
edges = (
    (0,1), (0,3), (0,4), (2,1), (2,3), (2,7),
    (6,3), (6,4), (6,7), (5,1), (5,4), (5,7)
)
# Positions for multiple cubes
cube_positions = [(0, 0, 0), (-3, 0, -5), (3, 0, -5), (0, 3, -5), (0, -3, -5)]

def draw_cube():
    glBegin(GL_LINES)
    glColor3f(0, 1, 0) # Bright Green
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

# --- GAME LOOP ---
while True:
    dt = clock.tick(60) / 1000
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # 2. Input Handling
    keys = pygame.key.get_pressed()
    speed = 5 * dt
    
    # Movement (Relative to Global Axis for simplicity)
    if keys[K_LEFT]:  cam_x += speed
    if keys[K_RIGHT]: cam_x -= speed
    if keys[K_UP]:    cam_z += speed
    if keys[K_DOWN]:  cam_z -= speed
    if keys[K_SPACE]: cam_y -= speed # Up
    if keys[K_LSHIFT]: cam_y += speed # Down
    if keys[K_q]: cam_yaw -= 90 * dt
    if keys[K_e]: cam_yaw += 90 * dt

    # 3. Render
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # Reset the "World" matrix before applying camera moves
    glLoadIdentity()
    
    # Apply Camera (Rotate Head -> Move World)
    glRotatef(cam_yaw, 0, 1, 0)
    glTranslatef(cam_x, cam_y, cam_z)

    # Draw Logic
    for pos in cube_positions:
        glPushMatrix() # Save current location (Camera pos)
        glTranslatef(pos[0], pos[1], pos[2]) # Move to Cube location
        draw_cube()
        glPopMatrix()  # Return to Camera pos for next loop

    pygame.display.flip()
```

### 5) 20-Minute Drill

Task: True Dungeon Movement

Currently, pressing UP moves you along the Global Z axis. If you turn your head (Q/E), UP still moves "North" instead of "Forward".

1. Import `math` at the top.
    
2. Change the `K_UP` and `K_DOWN` logic to use Sin/Cos:
    
    - `rad = math.radians(cam_yaw)`
        
    - `cam_x += math.sin(rad) * speed`
        
    - `cam_z += math.cos(rad) * speed`
        
    - _(You may need to flip signs `+=` or `-=` depending on direction)._
        

### 6) Quick Quiz

1. **What happens if we forget `glMatrixMode(GL_PROJECTION)` before setting `gluPerspective`?**
    
2. **Why do we use `glPushMatrix()` inside the cube loop?**
    
3. **To move the camera forward, do we add or subtract from the World Z?**
    

**Answers:**

1. The perspective math is applied to the objects instead of the lens, often causing a black screen or distorted geometry.
    
2. To "remember" where the camera was. If we didn't, the second cube would be drawn relative to the first cube, not the camera.
    
3. We **add** to the World Z (Move the world towards us).
    

### 7) Homework for Tomorrow

**Create a 3D Solar System.**

- Make the center cube Rotate (`glRotatef` inside the Push/Pop).
    
- Add a smaller cube that translates _away_ from the center and also rotates.
    
- See if you can make a Moon orbit the Earth (Nested `glPushMatrix`).
    

### 8) Progress to Mastery

🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜⬜⬜ **86%**

### 9) Obsidian Note

## 🧠 CONCEPT SUMMARY

#### Matrix Modes
OpenGL is a state machine with two main modes:
1.  **`GL_PROJECTION`**: The Lens. Sets FOV and Range. Set this **Once**.
2.  **`GL_MODELVIEW`**: The World. Sets position of objects. Set this **Every Frame**.

#### The Camera Illusion
To simulate a camera moving **Left**, we move the entire world **Right**.
To simulate moving **Forward**, we move the world **Back**.
> [!note] Order Matters
> 1. `glLoadIdentity()` (Reset)
> 2. `glRotatef()` (Camera Angle)
> 3. `glTranslatef()` (Camera Position)
> 4. Draw Objects

#### The Matrix Stack
* `glPushMatrix()`: Save current position (Bookmark).
* `glPopMatrix()`: Return to bookmark.
* **Usage:** Essential for drawing multiple independent objects without their coordinates adding up and drifting away.

---

## 🛠️ WHAT I DID TODAY
* **Fixed the Black Screen:** Learned to properly set `GL_PROJECTION` before defining the perspective.
* **Implemented 3D Movement:** Mapped keyboard inputs to `glTranslatef`.
* **Rendered Multiple Objects:** Used the Matrix Stack to place cubes at different coordinates in the same world.

---

## 💻 SOURCE CODE
> [!example]- CORRECT 3D SETUP
> ```python
> glMatrixMode(GL_PROJECTION)
> glLoadIdentity()
> gluPerspective(45, AspectRatio, 0.1, 50.0)
> 
> glMatrixMode(GL_MODELVIEW)
> glLoadIdentity()
> ```

---

## 🎯 GOALS FOR TOMORROW
> [!todo] 🧠 **Day 27: Advanced AI Behaviors**
> * Return to Game Logic.
> * Implement **Finite State Machines (FSM)**.
> * Create an enemy that transitions between **Patrol**, **Alert**, and **Attack** states based on vision cones.
