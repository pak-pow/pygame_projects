# visuals.py
import pygame
import random
import math
from config import *


class CrackDecal:
    """Jagged lines that appear on impact"""

    def __init__(self, wx, wy, color):
        self.wx = wx
        self.wy = wy
        self.color = color
        self.lifetime = 5.0  # Lasts 5 seconds
        self.points = []

        # Generate 3-5 jagged lines radiating from center
        num_branches = random.randint(3, 5)
        for _ in range(num_branches):
            angle = random.uniform(0, 6.28)
            length = random.uniform(1.5, 3.0)  # Length in world units

            # Start at center
            branch = [(0, 0)]
            curr_dist = 0

            # Create jagged segments
            while curr_dist < length:
                step = random.uniform(0.3, 0.6)
                curr_dist += step

                # Wiggle the angle slightly for "jagged" look
                wiggled_angle = angle + random.uniform(-0.5, 0.5)

                # Calculate offset relative to center
                px = branch[-1][0] + math.cos(wiggled_angle) * step
                py = branch[-1][1] + math.sin(wiggled_angle) * step
                branch.append((px, py))

            self.points.append(branch)

    def update(self, dt):
        self.lifetime -= dt

    def draw(self, surf, cam):
        if self.lifetime > 0:
            sx_start, sy_start = cam.world_to_screen(self.wx, self.wy)

            # Fade out
            alpha = int(255 * min(1.0, self.lifetime / 2.0))
            if alpha < 5: return

            # We need a temp surface for alpha lines if we want them to fade nicely,
            # but for sharp cracks, direct drawing is usually fine.
            # To support fading, we pick a color that gets darker.
            fade_col = (
                max(0, self.color[0] * (alpha / 255)),
                max(0, self.color[1] * (alpha / 255)),
                max(0, self.color[2] * (alpha / 255))
            )

            for branch in self.points:
                # Convert relative points to screen points
                screen_points = []
                for pt in branch:
                    wx = self.wx + pt[0]
                    wy = self.wy + pt[1]
                    screen_points.append(cam.world_to_screen(wx, wy))

                if len(screen_points) > 1:
                    pygame.draw.lines(surf, fade_col, False, screen_points, max(1, int(2 * cam.zoom)))


class GhostTrace:
    """Visual echo of the player when dashing"""

    def __init__(self, wx, wy, color, radius):
        self.wx = wx
        self.wy = wy
        self.color = color
        self.radius = radius
        self.alpha = 200
        self.lifetime = 0.5

    def update(self, dt):
        self.lifetime -= dt
        self.alpha = max(0, int((self.lifetime / 0.5) * 200))

    def draw(self, surf, cam):
        if self.lifetime > 0:
            sx, sy = cam.world_to_screen(self.wx, self.wy)
            s = pygame.Surface((self.radius * 2 * cam.zoom + 10, self.radius * 2 * cam.zoom + 10), pygame.SRCALPHA)
            cx, cy = s.get_width() // 2, s.get_height() // 2
            r_scaled = self.radius * cam.zoom
            pygame.draw.circle(s, (*self.color, self.alpha), (cx, cy), r_scaled)
            surf.blit(s, (sx - cx, sy - cy - (15 * cam.zoom)))


class Particle:
    def __init__(self, x, y, color, speed, lifetime, size_start):
        self.x = x
        self.y = y
        angle = random.uniform(0, 6.28)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed * 0.6
        self.color = color
        self.lifetime = lifetime
        self.max_life = lifetime
        self.size = size_start

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.lifetime -= dt
        self.size = max(0, self.size - (self.size / self.max_life) * dt)

    def draw(self, surf):
        if self.lifetime > 0:
            pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), int(self.size))


class ShellCasing:
    def __init__(self, wx, wy):
        self.wx = wx
        self.wy = wy
        self.z = 1.0
        angle = random.uniform(0, 6.28)
        speed = random.uniform(2.0, 4.0)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.vz = random.uniform(8.0, 12.0)
        self.lifetime = 10.0
        self.bounces = 0

    def update(self, dt):
        if self.z > 0 or self.vz > 0:
            self.vz -= 30.0 * dt
            self.wx += self.vx * dt * 2.0
            self.wy += self.vy * dt * 2.0
            self.z += self.vz * dt
            if self.z < 0:
                self.z = 0
                self.vz = -self.vz * 0.6
                self.vx *= 0.8
                self.vy *= 0.8
                self.bounces += 1
                if abs(self.vz) < 1.0:
                    self.vz = 0
        else:
            self.lifetime -= dt

    def draw(self, surf, cam):
        sx, sy = cam.world_to_screen(self.wx, self.wy)
        draw_y = sy - (self.z * 15 * cam.zoom)
        col = (255, 200, 50)
        if self.bounces % 2 == 0:
            col = (200, 150, 20)
        w, h = 3 * cam.zoom, 5 * cam.zoom
        pygame.draw.rect(surf, (0, 0, 0), (sx, sy, w + 1, 2 * cam.zoom))
        pygame.draw.rect(surf, col, (sx, draw_y, w, h))


class Debris:
    def __init__(self, wx, wy, d_type, level_color):
        self.wx = wx
        self.wy = wy
        self.type = d_type
        self.scale = random.uniform(0.8, 1.2)
        self.color = level_color
        self.lifetime = 10.0

    def update(self, dt):
        self.lifetime -= dt

    def draw(self, surf, cam):
        sx, sy = cam.world_to_screen(self.wx, self.wy)
        if self.type == "blood":
            pygame.draw.ellipse(surf, (100, 0, 0),
                                (sx - 10 * self.scale, sy - 5 * self.scale, 20 * self.scale, 10 * self.scale))
        elif self.type == "robot_parts":
            c = (self.color[0] * 0.5, self.color[1] * 0.5, self.color[2] * 0.5)
            pygame.draw.rect(surf, c, (sx, sy, 8, 8))


class FloatingText:
    def __init__(self, x, y, text, color, duration=1.0, size=20):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.duration = duration
        self.timer = 0.0
        self.vy = -30
        self.size = size

    def update(self, dt):
        self.timer += dt
        self.y += self.vy * dt

    def draw(self, surf, font_dict):
        if self.timer < self.duration:
            font = font_dict.get(self.size, font_dict[20])
            lbl = font.render(self.text, True, self.color)
            outline = font.render(self.text, True, (0, 0, 0))
            surf.blit(outline, (self.x - lbl.get_width() // 2 + 1, self.y + 1))
            surf.blit(lbl, (self.x - lbl.get_width() // 2, self.y))


class VisualManager:
    def __init__(self):
        self.particles = []
        self.texts = []
        self.casings = []
        self.debris = []
        self.ghosts = []
        self.cracks = []  # NEW: Jagged cracks
        self.fonts = {
            16: pygame.font.SysFont("Consolas", 16, bold=True),
            20: pygame.font.SysFont("Verdana", 20, bold=True),
            30: pygame.font.SysFont("Verdana", 30, bold=True)
        }

    def add_particle(self, x, y, color):
        p = Particle(x, y, color, random.uniform(20, 100), random.uniform(0.3, 0.8), random.uniform(3, 6))
        self.particles.append(p)

    def add_explosion(self, x, y, color=(255, 100, 50)):
        for _ in range(15):
            p = Particle(x, y, color, random.uniform(50, 150), random.uniform(0.5, 1.0), random.uniform(5, 10))
            self.particles.append(p)
        for _ in range(5):
            p = Particle(x, y, (100, 100, 100), random.uniform(20, 80), 1.5, 8)
            self.particles.append(p)

    def add_text(self, x, y, msg, color=(255, 255, 255), duration=1.0, size=20):
        self.texts.append(FloatingText(x, y, msg, color, duration, size))

    def add_casing(self, wx, wy):
        self.casings.append(ShellCasing(wx, wy))

    def add_debris(self, wx, wy, d_type, col=(100, 100, 100)):
        self.debris.append(Debris(wx, wy, d_type, col))

    def add_ghost(self, wx, wy, color, radius):
        self.ghosts.append(GhostTrace(wx, wy, color, radius))

    def add_crack(self, wx, wy, color=(200, 200, 200)):
        self.cracks.append(CrackDecal(wx, wy, color))

    def update(self, dt):
        for p in self.particles: p.update(dt)
        for t in self.texts: t.update(dt)
        for c in self.casings: c.update(dt)
        for d in self.debris: d.update(dt)
        for g in self.ghosts: g.update(dt)
        for k in self.cracks: k.update(dt)

        self.particles = [p for p in self.particles if p.lifetime > 0]
        self.texts = [t for t in self.texts if t.timer < t.duration]
        self.casings = [c for c in self.casings if c.lifetime > 0]
        self.debris = [d for d in self.debris if d.lifetime > 0]
        self.ghosts = [g for g in self.ghosts if g.lifetime > 0]
        self.cracks = [k for k in self.cracks if k.lifetime > 0]

    def draw_floor(self, surf, cam):
        for d in self.debris: d.draw(surf, cam)
        for k in self.cracks: k.draw(surf, cam)  # Draw cracks on floor

    def draw_ghosts(self, surf, cam):
        for g in self.ghosts: g.draw(surf, cam)

    def draw_top(self, surf, cam):
        for c in self.casings: c.draw(surf, cam)
        for p in self.particles: p.draw(surf)
        for t in self.texts: t.draw(surf, self.fonts)