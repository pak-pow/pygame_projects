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

        # Movement with WASD (relative to camera direction)
        rad = math.radians(self.yaw)
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