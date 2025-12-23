Tags: [[Programming]], [[Python]], [[PyGame]], [[Game]], [[OpenGL]]

---
### 1) Learning Goal

You will learn to setup a **3D Rendering Context** in Pygame, understand **Vertices** (points in 3D space) and **Edges** (connections), and render a rotating **Wireframe Cube**.

### 2) Clear Overview

- **The Z-Axis:** In 2D, we had X (Left/Right) and Y (Up/Down). In 3D, we add **Z** (Depth/Forward/Backward).
    
- **The Pipeline:**
    
    1. Define Points (Vertices).        
    2. Define Connections (Edges).
    3. Tell the GPU: "Draw lines between these points."
    
- The Library: You generally need to install it first: `pip install PyOpenGL PyOpenGL_accelerate`

### 3) Deep Explanation

**A. Vertices & Edges**

A Cube has 8 corners. We define them as coordinates (x, y, z).

- `(1, -1, -1)` is Bottom-Right-Back.
- `(-1, 1, 1)` is Top-Left-Front.

We store these in a **List of Tuples**.

**B. The Camera (gluPerspective)**

In 2D, we just see the screen. In 3D, we need a "Lens".

- **FOV (Field of View):** How wide the lens is (usually 45 degrees).
- **Aspect Ratio:** Width / Height.
- **Clipping Planes:** "Don't draw things too close (0.1) or too far (50.0)."

**C. The Draw Loop**

- We don't use screen.fill(). We use glClear().
- We don't use blit(). We use glBegin() and glEnd().

### 4) Runnable Pygame Code Example

**Controls:**

- The Cube rotates automatically. 
- It is a pure wireframe (lines only).

``` Python
import pygame
from pygame.locals import *

# OpenGL Imports
from OpenGL.GL import *
from OpenGL.GLU import *

# 1. Setup
pygame.init()
display = (800, 600)

# DOUBLEBUF: specialized video buffer for smooth 3D
# OPENGL: Tells Pygame we aren't doing 2D blitting
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# 2. Camera Setup
# (FOV, Aspect Ratio, Near Clip, Far Clip)
gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

# Move the camera BACK 5 units so we can see the cube
# (x, y, z) -> Moving -5 in Z pulls us away from the object
glTranslatef(0.0, 0.0, -5)

# --- THE CUBE DATA ---
# 8 Corner points (x, y, z)
vertices = (
    (1, -1, -1),  (1, 1, -1),
    (-1, 1, -1), (-1, -1, -1),
    (1, -1, 1),   (1, 1, 1),
    (-1, -1, 1),  (-1, 1, 1)
)

# Pairs of indices (Which vertices connect to which?)
edges = (
    (0,1), (0,3), (0,4),
    (2,1), (2,3), (2,7),
    (6,3), (6,4), (6,7),
    (5,1), (5,4), (5,7)
)

def draw_cube():
    glBegin(GL_LINES) # Start drawing Lines
    for edge in edges:
        for vertex in edge:
            # Send the vertex data to the GPU
            glVertex3fv(vertices[vertex])
    glEnd() # Stop drawing

# --- MAIN LOOP ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # 1. Rotate
    # (Angle, x_axis, y_axis, z_axis)
    # Rotate 1 degree per frame on the X and Y axes
    glRotatef(1, 3, 1, 1)

    # 2. Clear Screen
    # Clear both the Color Buffer (Pixels) and Depth Buffer (Layers)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # 3. Draw
    draw_cube()

    # 4. Flip
    pygame.display.flip()
    # Simple wait to cap FPS (clock.tick doesn't work perfectly with OpenGL context sometimes)
    pygame.time.wait(10)
```

### 5) 20-Minute Drill

**Task: Make it Solid (Quads)**

1. Define a new tuple called `surfaces`. A cube has 6 faces. Each face needs **4 vertex indices** (e.g., `(0,1,2,3)`). _Hint: Look at the vertices list and visualize the squares._
    
2. In `draw_cube`, add a new block **before** `GL_LINES`.
    
3. Use `glBegin(GL_QUADS)`.
    
4. Loop through your `surfaces` list and pass `glVertex3fv`.
    
5. **Color:** Before passing vertices, call `glColor3fv((0, 1, 0))` to make the faces Green.
    

### 6) Quick Quiz

1. **What coordinate do we change to move an object "further away" from the camera?**
    
2. **What happens if we forget `glClear(GL_COLOR_BUFFER_BIT)`?**
    
3. **Why do we use `GL_LINES` for the first example instead of `GL_QUADS`?**
    

**Answers:**

1. The **Z** coordinate (usually negative Z goes into the screen).
    
2. The previous frames "smear" across the screen (the "Hall of Mirrors" effect).
    
3. It creates a "Wireframe," which is easier to debug and understand than a solid shape for beginners.
    

### 7) Homework for Tomorrow

**Create a Solar System.**

- Instead of one cube, draw **two**.
    
- Use `glPushMatrix()` and `glPopMatrix()` (we will cover this deeply tomorrow, but try to look it up).
    
- Make a small cube "orbit" around a large cube.
    

### 8) Progress to Mastery

🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜⬜⬜⬜ **83%**

### 9) Obsidian Note

## 🧠 CONCEPT SUMMARY

#### The Z-Axis
We now define points as `(x, y, z)`.
* **X:** Left/Right
* **Y:** Up/Down
* **Z:** Depth (Into/Out of screen)

#### The Rendering Pipeline
Unlike 2D blitting (copying pixels), 3D rendering involves:
1.  **Vertices:** The corner points.
2.  **Primitives:** How we connect them (`GL_LINES` vs `GL_QUADS`).
3.  **Projection:** Transforming 3D space onto a 2D monitor (`gluPerspective`).

#### Key OpenGL Commands
* `glTranslatef(x, y, z)`: Moves the "pen" (or the world) to a new location.
* `glRotatef(angle, x, y, z)`: Rotates the world around a specific axis.
* `glBegin(MODE)` / `glEnd()`: The bracket functions where actual drawing happens.

---

## 🛠️ WHAT I DID TODAY
* **Installed PyOpenGL:** Connected Python to the GPU driver.
* **Defined a Mesh:** Created a Cube using a list of 8 vertices and 12 edges.
* **Rendered Wireframe:** Used `GL_LINES` to draw the skeleton of a 3D object.

---

## 💻 SOURCE CODE
> [!example]- BASIC CUBE DATA
> ```python
> vertices = (
>     (1, -1, -1), (1, 1, -1),
>     (-1, 1, -1), (-1, -1, -1),
>     (1, -1, 1), (1, 1, 1),
>     (-1, -1, 1), (-1, 1, 1)
> )
> ```

---

## 🎯 GOALS FOR TOMORROW
> [!todo] 🎥 **Day 26: 3D Camera Movement**
> * Learn `glPushMatrix` and `glPopMatrix` (The Matrix Stack).
> * Move the camera with WASD (First Person controls).
> * Understand Local Space vs. World Space.
