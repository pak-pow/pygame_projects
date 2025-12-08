# camera.py
import random
import math
from config import *


class Camera:
    def __init__(self, width, height):
        self.w = width
        self.h = height

        # Focus Point (World Coordinates)
        self.focus_wx = 0.0
        self.focus_wy = 0.0
        self.target_wx = 0.0
        self.target_wy = 0.0

        self.zoom = 1.0
        self.target_zoom = 1.0

        # ROTATION ANIMATION VARIABLES
        self.angle = 0.0  # The current visual angle (smooth)
        self.target_angle = 0.0  # The angle we want to reach
        self.rotation_index = 0  # 0, 1, 2, 3 (Used for WASD logic in main.py)

        self.shake_timer = 0.0
        self.shake_mag = 0.0
        self.shake_offset_x = 0
        self.shake_offset_y = 0

    def rotate_view(self):
        # Update the logical index (for controls)
        self.rotation_index = (self.rotation_index + 1) % 4
        # Add 90 degrees (pi/2 radians) to the target
        self.target_angle += math.pi / 2

    def add_shake(self, amount):
        self.shake_mag = min(self.shake_mag + amount, 30.0)
        self.shake_timer = 0.3

    def zoom_in(self):
        self.target_zoom = min(self.target_zoom + 0.1, ZOOM_MAX)

    def zoom_out(self):
        self.target_zoom = max(self.target_zoom - 0.1, ZOOM_MIN)

    def set_target(self, wx, wy):
        self.target_wx = wx
        self.target_wy = wy

    def update(self, dt):
        # 1. Smoothly interpolate Focus Point and Zoom
        speed = 5.0
        self.focus_wx += (self.target_wx - self.focus_wx) * speed * dt
        self.focus_wy += (self.target_wy - self.focus_wy) * speed * dt
        self.zoom += (self.target_zoom - self.zoom) * speed * dt

        # 2. Smoothly interpolate Rotation Angle
        # "10.0" is the rotation speed. Higher = faster snap.
        diff = self.target_angle - self.angle
        self.angle += diff * 10.0 * dt

        # 3. Handle Shake
        if self.shake_timer > 0:
            self.shake_timer -= dt
            self.shake_offset_x = random.uniform(-self.shake_mag, self.shake_mag)
            self.shake_offset_y = random.uniform(-self.shake_mag, self.shake_mag)
            self.shake_mag = max(0, self.shake_mag - 60 * dt)
        else:
            self.shake_offset_x = 0
            self.shake_offset_y = 0

    def world_to_screen(self, wx, wy):
        tile_w = TILE_W_BASE * self.zoom
        tile_h = TILE_H_BASE * self.zoom

        # A. Center coordinates relative to camera focus
        rx = wx - self.focus_wx
        ry = wy - self.focus_wy

        # B. Apply Smooth Rotation (Trigonometry)
        c = math.cos(self.angle)
        s = math.sin(self.angle)

        # Standard 2D rotation formula
        rot_x = rx * c - ry * s
        rot_y = rx * s + ry * c

        # C. Isometric Projection (on the rotated coordinates)
        iso_x = (rot_x - rot_y) * (tile_w / 2.0)
        iso_y = (rot_x + rot_y) * (tile_h / 2.0)

        # D. Screen Offset & Shake
        final_sx = iso_x + (self.w / 2.0) + self.shake_offset_x
        final_sy = iso_y + (self.h / 2.0) + self.shake_offset_y

        return final_sx, final_sy

    def screen_to_world(self, sx, sy):
        tile_w = TILE_W_BASE * self.zoom
        tile_h = TILE_H_BASE * self.zoom

        # A. Remove Screen Offset & Shake
        adj_x = sx - (self.w / 2.0) - self.shake_offset_x
        adj_y = sy - (self.h / 2.0) - self.shake_offset_y

        # B. Inverse Isometric Projection
        # Solve for rot_x, rot_y
        val_x = adj_x / (tile_w / 2.0)
        val_y = adj_y / (tile_h / 2.0)

        rot_x = (val_x + val_y) / 2.0
        rot_y = (val_y - val_x) / 2.0

        # C. Inverse Rotation
        # To invert the rotation, we rotate by -angle (or just use transposed matrix)
        c = math.cos(self.angle)
        s = math.sin(self.angle)

        # Inverse rotation formula
        rx = rot_x * c + rot_y * s
        ry = -rot_x * s + rot_y * c

        # D. Add Focus Point back
        wx = rx + self.focus_wx
        wy = ry + self.focus_wy

        return wx, wy