import pygame
import sys

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

class Main:

    DISPLAY_WIDTH = 800
    DISPLAY_HEIGHT = 600
    CLOCK = pygame.time.Clock()
    FPS = 60

    def __init__(self):

        pygame.init()
        self.display = (self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT)
        self.DISPLAY = pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        pygame.display.set_caption("DAY 26")

        # ========OPENGL SETUP============
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, self.display[0] / self.display[1], 0.1, 50.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glEnable(GL_DEPTH_TEST)

        # ==========CAMERA==============
        self.cam_x = 0
        self.cam_y = 0
        self.cam_z = -5
        self.cam_yaw = 0

        # ============Cube Data=========
        self.vertices = (
            (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
            (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1)
        )

        self.edges = (
            (0, 1), (0, 3), (0, 4), (2, 1), (2, 3), (2, 7),
            (6, 3), (6, 4), (6, 7), (5, 1), (5, 4), (5, 7)
        )

        self.cube_positions = [
            (0, 0, 0),
            (-3, 0, -5),
            (3, 0, -5),
            (0, 3, -5),
            (0, -3, -5)
        ]

    def draw_cube(self):

        glBegin(GL_LINES)
        glColor3f(1, 1, 0)

        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
        glEnd()

    def handle_input(self, dt):
        keys = pygame.key.get_pressed()
        speed = 5 * dt

        if keys[K_a]:
            self.cam_x += speed

        if keys[K_d]:
            self.cam_x -= speed

        if keys[K_w]:
            self.cam_z += speed

        if keys[K_s]:
            self.cam_z -= speed

        if keys[K_SPACE]:
            self.cam_y -= speed

        if keys[K_LSHIFT]:
            self.cam_y += speed

        if keys[K_q]:
            self.cam_yaw -= 90 * dt

        if keys[K_e]:
            self.cam_yaw += 90 * dt


    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glRotatef(self.cam_yaw, 0, 1, 0)
        glTranslatef(self.cam_x, self.cam_y, self.cam_z)

        for pos in self.cube_positions:
            glPushMatrix()
            glTranslatef(pos[0], pos[1], pos[2])
            self.draw_cube()
            glPopMatrix()

        pygame.display.flip()

    def run(self):

        while True:
            dt = self.CLOCK.tick(self.FPS) / 1000

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    quit()

            self.handle_input(dt)
            self.render()


if __name__ == "__main__":
    app = Main()
    app.run()