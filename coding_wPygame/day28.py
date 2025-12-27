import pygame, math
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


# 1. THE CONFIG CLASS (Tweakables)
class Config:
    fov = 45.0
    move_speed = 5.0
    mouse_sens = 2.0

    # Constraints
    min_fov = 10.0
    max_fov = 120.0
    min_speed = 1.0
    max_speed = 20.0


# Setup
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
clock = pygame.time.Clock()


# --- HELPER: Update Lens ---
def update_projection():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Use Config.fov here!
    gluPerspective(Config.fov, (display[0] / display[1]), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)


# Initial Setup
update_projection()

# State
cam_x, cam_y, cam_z = 0, 0, -5
cam_yaw = 0

# Cube Data
vertices = (
    (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
    (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1)
)
edges = ((0, 1), (0, 3), (0, 4), (2, 1), (2, 3), (2, 7), (6, 3), (6, 4), (6, 7), (5, 1), (5, 4), (5, 7))


def draw_grid():

    glBegin(GL_LINES)
    glColor3f(0.3, 0.3, 0.3)

    for i in range(-10, 11):

        glVertex3f(i, -1, -10)
        glVertex3f(i, -1, 10)
        glVertex3f(-10, -1, i)
        glVertex3f(10, -1, i)

    glEnd()


def draw_cube():
    glBegin(GL_LINES)
    glColor3f(1, 1, 0)  # Yellow
    for edge in edges:
        for v in edge:
            glVertex3fv(vertices[v])
    glEnd()


while True:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # --- REAL-TIME BALANCING INPUTS ---
    keys = pygame.key.get_pressed()

    # Adjust FOV (The "Zoom" Effect)
    if keys[K_UP]:
        Config.fov += 20 * dt
        if Config.fov > Config.max_fov: Config.fov = Config.max_fov
        update_projection()  # Apply change immediately

    if keys[K_DOWN]:
        Config.fov -= 20 * dt
        if Config.fov < Config.min_fov: Config.fov = Config.min_fov
        update_projection()

    # Adjust Speed
    if keys[K_RIGHT]:
        Config.move_speed += 5 * dt
    if keys[K_LEFT]:
        Config.move_speed -= 5 * dt
        if Config.move_speed < Config.min_speed: Config.move_speed = Config.min_speed

    # --- STANDARD MOVEMENT ---
    if keys[K_q]: cam_yaw -= 90 * dt
    if keys[K_e]: cam_yaw += 90 * dt

    rad = math.radians(cam_yaw)
    if keys[K_w]:
        cam_x += math.sin(rad) * Config.move_speed * dt
        cam_z -= math.cos(rad) * Config.move_speed * dt
    if keys[K_s]:
        cam_x -= math.sin(rad) * Config.move_speed * dt
        cam_z += math.cos(rad) * Config.move_speed * dt

    # --- DEBUG UI (Window Title) ---
    caption = f"FOV: {int(Config.fov)} | Speed: {Config.move_speed:.1f} | FPS: {int(clock.get_fps())}"
    pygame.display.set_caption(caption)

    # --- RENDER ---
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Camera
    glRotatef(-cam_yaw, 0, 1, 0)
    glTranslatef(-cam_x, -cam_y, -cam_z)

    draw_grid()
    draw_cube()  # Drawn at 0,0,0

    pygame.display.flip()