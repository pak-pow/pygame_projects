# entities.py
import math
import random
import pygame
from config import *
from utils import clamp, check_grid_collision, has_line_of_sight, get_path_bfs, distance

class Bullet:
    def __init__(self, wx, wy, vx, vy, speed, damage, pierce_count, color, owner_id):
        self.wx = wx
        self.wy = wy
        l = math.hypot(vx, vy)
        if l == 0: l = 1
        self.vx = (vx / l) * speed
        self.vy = (vy / l) * speed
        self.damage = damage
        self.pierce = pierce_count
        self.lifetime = 3.0
        self.radius = 5
        self.hit_list = []
        self.color = color
        self.owner_id = owner_id

    def update(self, dt):
        self.wx += self.vx * dt
        self.wy += self.vy * dt
        self.lifetime -= dt

    def draw(self, surf, cam):
        sx, sy = cam.world_to_screen(self.wx, self.wy)
        r = self.radius * cam.zoom
        pygame.draw.circle(surf, (255, 200, 50), (sx, sy), r + 2, 1)
        pygame.draw.circle(surf, self.color, (sx, sy), r)

class Grenade:
    def __init__(self, start_x, start_y, target_x, target_y):
        self.x = start_x
        self.y = start_y
        self.z = 15

        # Heavier grenade throw
        max_throw = 6.0
        dist = distance(start_x, start_y, target_x, target_y)
        if dist > max_throw:
            angle = math.atan2(target_y - start_y, target_x - start_x)
            target_x = start_x + math.cos(angle) * max_throw
            target_y = start_y + math.sin(angle) * max_throw
            dist = max_throw

        speed_xy = 8.0
        angle = math.atan2(target_y - start_y, target_x - start_x)
        self.vx = math.cos(angle) * speed_xy
        self.vy = math.sin(angle) * speed_xy
        self.vz = 20 + (dist * 2.0)
        self.timer = 2.0
        self.exploded = False
        self.radius = 4.0

    def update(self, dt, grid):
        if self.exploded:
            return

        next_x = self.x + self.vx * dt
        next_y = self.y + self.vy * dt

        if check_grid_collision(next_x, self.y, grid):
            self.vx = -self.vx * 0.6
        else:
            self.x = next_x

        if check_grid_collision(self.x, next_y, grid):
            self.vy = -self.vy * 0.6
        else:
            self.y = next_y

        self.z += self.vz * dt
        self.vz -= GRAVITY * 2 * dt

        if self.z < 0:
            self.z = 0
            self.vz = -self.vz * 0.5
            self.vx *= 0.4
            self.vy *= 0.4
            if abs(self.vx) < 0.1: self.vx = 0
            if abs(self.vy) < 0.1: self.vy = 0

        self.timer -= dt
        if self.timer <= 0:
            self.exploded = True

    def draw(self, surf, cam):
        sx, sy = cam.world_to_screen(self.x, self.y)
        pygame.draw.circle(surf, (0,0,0), (sx, sy), 5 * cam.zoom)
        z_offset = self.z * TILE_H_BASE/2 * cam.zoom
        pygame.draw.circle(surf, COL_GRENADE, (sx, sy - z_offset), 6 * cam.zoom)
        if self.timer < 0.5 and (int(self.timer * 20) % 2 == 0):
            pygame.draw.circle(surf, (255, 255, 255), (sx, sy - z_offset), 6 * cam.zoom)

class Entity:
    def __init__(self, wx, wy):
        self.wx = wx
        self.wy = wy
        self.z = 0
        self.radius = 0.4
        self.dead = False
        self.uid = id(self)
        self.knockback_x = 0
        self.knockback_y = 0

    def get_sort_y(self):
        return self.wx + self.wy

    def apply_knockback(self, kx, ky):
        self.knockback_x += kx
        self.knockback_y += ky

    def physics_update(self, dt):
        self.wx += self.knockback_x * dt
        self.wy += self.knockback_y * dt
        fric = 5.0
        self.knockback_x -= self.knockback_x * fric * dt
        self.knockback_y -= self.knockback_y * fric * dt
        if abs(self.knockback_x) < 0.1: self.knockback_x = 0
        if abs(self.knockback_y) < 0.1: self.knockback_y = 0

        # --- FIX STARTS HERE ---
    def check_wall_collision(self, dx, dy, grid):
            """
            Updated to check the 'leading edge' of the entity based on radius.
            This prevents the sprite from clipping halfway into walls.
            """
            margin = self.radius

            # 1. Try Moving X
            # We determine which side of the player is "leading" the movement
            if dx > 0:
                check_x = self.wx + dx + margin
            else:
                check_x = self.wx + dx - margin

            # Check if that edge hits a wall
            if not check_grid_collision(check_x, self.wy, grid):
                self.wx += dx

            # 2. Try Moving Y
            if dy > 0:
                check_y = self.wy + dy + margin
            else:
                check_y = self.wy + dy - margin

            # Check if that edge hits a wall
            if not check_grid_collision(self.wx, check_y, grid):
                self.wy += dy

            # Clamp to map boundaries (keeping radius inside)
            self.wx = clamp(self.wx, 0.5 + margin, MAP_W - 0.5 - margin)
            self.wy = clamp(self.wy, 0.5 + margin, MAP_H - 0.5 - margin)

        # --- FIX ENDS HERE ---

    def draw_shadow(self, surf, cam):
            sx, sy = cam.world_to_screen(self.wx, self.wy)
            shadow_w = 30 * cam.zoom
            shadow_h = 10 * cam.zoom
            pygame.draw.ellipse(surf, (0, 0, 0, 100), (sx - shadow_w // 2, sy + shadow_h // 2, shadow_w, shadow_h))

    def draw(self, surf, cam):
        pass

class WallBlock(Entity):
    def __init__(self, wx, wy, color_top, color_side):
        super().__init__(wx, wy)
        self.color_top = color_top
        self.color_side = color_side
        self.wx = wx + 0.5
        self.wy = wy + 0.5

    def draw_shadow(self, surf, cam):
        pass

    def draw(self, surf, cam):
        sx, sy = cam.world_to_screen(self.wx - 0.5, self.wy - 0.5)
        tile_w = TILE_W_BASE * cam.zoom
        tile_h = TILE_H_BASE * cam.zoom
        wall_h = 30 * cam.zoom

        p_top = [
            (sx, sy - wall_h),
            (sx + tile_w//2, sy + tile_h//2 - wall_h),
            (sx, sy + tile_h - wall_h),
            (sx - tile_w//2, sy + tile_h//2 - wall_h)
        ]
        p_right = [
            (sx, sy + tile_h - wall_h),
            (sx + tile_w//2, sy + tile_h//2 - wall_h),
            (sx + tile_w//2, sy + tile_h//2),
            (sx, sy + tile_h)
        ]
        p_left = [
            (sx - tile_w//2, sy + tile_h//2 - wall_h),
            (sx, sy + tile_h - wall_h),
            (sx, sy + tile_h),
            (sx - tile_w//2, sy + tile_h//2)
        ]

        pygame.draw.polygon(surf, self.color_side, p_right)
        pygame.draw.polygon(surf, self.color_side, p_left)
        pygame.draw.polygon(surf, self.color_top, p_top)
        pygame.draw.polygon(surf, (0,0,0), p_top, 1)

# --- ENEMIES ---
class Enemy(Entity):
    def __init__(self, wx, wy, level, vm):
        super().__init__(wx, wy)
        self.vm = vm
        self.level_scaling = level
        self.max_health = 10
        self.health = 10
        self.speed = 2.5 + (level * 0.15)
        self.money_value = 5
        self.color = (200, 50, 50)
        self.damage_to_player = 10
        self.flash_timer = 0.0
        self.debris_type = "blood"
        self.path = []
        self.path_timer = 0.0

    def take_damage(self, amt):
        self.health -= amt
        self.flash_timer = 0.1
        if self.health <= 0:
            self.dead = True
            self.vm.add_debris(self.wx, self.wy, self.debris_type, self.color)

    def update(self, dt, player, grid):
        self.physics_update(dt)
        if self.flash_timer > 0:
            self.flash_timer -= dt

        if abs(self.knockback_x) + abs(self.knockback_y) < 2.0:
            if has_line_of_sight(self.wx, self.wy, player.wx, player.wy, grid):
                self.path = []
                dx = player.wx - self.wx
                dy = player.wy - self.wy
                dist = math.hypot(dx, dy)
                if dist > 0.1:
                    self.move_towards(dx, dy, dist, dt, grid)
            else:
                self.path_timer -= dt
                if self.path_timer <= 0:
                    self.path_timer = 0.5
                    if distance(self.wx, self.wy, player.wx, player.wy) > 1.0:
                        self.path = get_path_bfs((int(self.wx), int(self.wy)), (int(player.wx), int(player.wy)), grid)
                    else:
                        self.path = []

                target_wx, target_wy = player.wx, player.wy
                if self.path:
                    next_node = self.path[0]
                    tx, ty = next_node[0] + 0.5, next_node[1] + 0.5
                    if distance(self.wx, self.wy, tx, ty) < 0.2:
                        self.path.pop(0)
                    else:
                        target_wx, target_wy = tx, ty

                dx = target_wx - self.wx
                dy = target_wy - self.wy
                dist = math.hypot(dx, dy)
                if dist > 0.1:
                    self.move_towards(dx, dy, dist, dt, grid)

    def move_towards(self, dx, dy, dist, dt, grid):
        move_step = self.speed * dt
        vx = (dx/dist) * move_step
        vy = (dy/dist) * move_step
        self.check_wall_collision(vx, vy, grid)

    def draw(self, surf, cam):
        sx, sy = cam.world_to_screen(self.wx, self.wy)
        col = (255, 255, 255) if self.flash_timer > 0 else self.color
        r = 16 * cam.zoom
        pygame.draw.circle(surf, col, (sx, sy - r), r)
        self.draw_hp(surf, sx, sy - r*2.5, cam.zoom)

    def draw_hp(self, surf, sx, sy, zoom):
        pct = clamp(self.health / self.max_health, 0, 1)
        w = 30 * zoom
        h = 6 * zoom
        pygame.draw.rect(surf, (0,0,0), (sx - w//2, sy, w, h))
        pygame.draw.rect(surf, (50, 200, 50), (sx - w//2 + 1, sy+1, int((w-2)*pct), h-2))

class OrbEnemy(Enemy):
    def __init__(self, wx, wy, level, vm):
        super().__init__(wx, wy, level, vm)
        self.max_health = 15 + level * 5
        self.health = self.max_health
        self.speed = 2.8 + (level * 0.15)
        self.color = (200, 60, 60)
        self.money_value = 10 + level

    def draw(self, surf, cam):
        sx, sy = cam.world_to_screen(self.wx, self.wy)
        col = (255, 255, 255) if self.flash_timer > 0 else self.color
        r = 18 * cam.zoom
        pygame.draw.circle(surf, col, (sx, sy - r), r)
        pygame.draw.circle(surf, (255,100,100), (sx - 5*cam.zoom, sy - 20*cam.zoom), 5*cam.zoom)
        self.draw_hp(surf, sx, sy - r*2.5, cam.zoom)

class BlockEnemy(Enemy):
    def __init__(self, wx, wy, level, vm):
        super().__init__(wx, wy, level, vm)
        self.max_health = 40 + level * 10
        self.health = self.max_health
        self.speed = 1.5 + (level * 0.1)
        self.radius = 25
        self.color = (60, 100, 200)
        self.money_value = 25 + level * 2
        self.debris_type = "robot_parts"

    def draw(self, surf, cam):
        sx, sy = cam.world_to_screen(self.wx, self.wy)
        col = (255, 255, 255) if self.flash_timer > 0 else self.color
        s = 40 * cam.zoom
        rect = pygame.Rect(0, 0, s, s)
        rect.center = (sx, sy - s//2)
        pygame.draw.rect(surf, col, rect)
        pygame.draw.rect(surf, (20,20,50), rect, int(2*cam.zoom))
        self.draw_hp(surf, sx, sy - s - 10, cam.zoom)

class SpikeEnemy(Enemy):
    def __init__(self, wx, wy, level, vm):
        super().__init__(wx, wy, level, vm)
        self.max_health = 8 + level * 3
        self.health = self.max_health
        self.speed = 4.0 + (level * 0.2)
        self.color = (200, 200, 50)
        self.money_value = 15 + level
        self.move_timer = 0
        self.move_dir = (0,0)

    def move_towards(self, dx, dy, dist, dt, grid):
        self.move_timer -= dt
        if self.move_timer <= 0:
            self.move_timer = random.uniform(0.3, 0.8)
            angle = math.atan2(dy, dx) + random.uniform(-1.0, 1.0)
            self.move_dir = (math.cos(angle), math.sin(angle))

        vx = self.move_dir[0] * self.speed * dt
        vy = self.move_dir[1] * self.speed * dt
        self.check_wall_collision(vx, vy, grid)

    def draw(self, surf, cam):
        sx, sy = cam.world_to_screen(self.wx, self.wy)
        col = (255, 255, 255) if self.flash_timer > 0 else self.color
        h = 40 * cam.zoom
        w = 15 * cam.zoom
        p1 = (sx, sy - h)
        p2 = (sx - w, sy)
        p3 = (sx + w, sy)
        pygame.draw.polygon(surf, col, [p1, p2, p3])
        self.draw_hp(surf, sx, sy - h - 10, cam.zoom)

class HexBoss(Enemy):
    def __init__(self, wx, wy, level, vm):
        super().__init__(wx, wy, level, vm)
        self.max_health = 300 + level * 50
        self.health = self.max_health
        self.speed = 1.2 + (level * 0.05)
        self.radius = 40
        self.color = (150, 50, 200)
        self.money_value = 500
        self.damage_to_player = 30
        self.debris_type = "scorch"

    def draw(self, surf, cam):
        sx, sy = cam.world_to_screen(self.wx, self.wy)
        col = (255, 255, 255) if self.flash_timer > 0 else self.color
        pts = []
        radius = 35 * cam.zoom
        for i in range(6):
            ang = math.radians(i * 60)
            px = sx + math.cos(ang) * radius
            py = (sy - 20*cam.zoom) + math.sin(ang) * radius * 0.7
            pts.append((px, py))
        pygame.draw.polygon(surf, col, pts)
        pygame.draw.polygon(surf, (255,255,255), pts, int(3*cam.zoom))
        self.draw_hp(surf, sx, sy - 70*cam.zoom, cam.zoom)

# --- DRONE ---
class Drone:
    def __init__(self, player, index, total_drones):
        self.player = player
        self.index = index
        self.total = total_drones
        self.angle_offset = (6.28 / total_drones) * index
        self.dist = 1.5
        self.rotation_speed = 2.0
        self.wx = 0
        self.wy = 0
        self.last_shot = 0
        self.fire_rate = 2.0
        self.damage = 5

    def update(self, dt, enemies, bullet_list):
        self.angle_offset += self.rotation_speed * dt
        self.wx = self.player.wx + math.cos(self.angle_offset) * self.dist
        self.wy = self.player.wy + math.sin(self.angle_offset) * self.dist
        self.last_shot += dt
        if self.last_shot >= 1.0 / self.fire_rate:
            closest = None
            min_d = 10.0
            for e in enemies:
                d = distance(self.wx, self.wy, e.wx, e.wy)
                if d < min_d:
                    min_d = d
                    closest = e
            if closest:
                self.last_shot = 0
                dx = closest.wx - self.wx
                dy = closest.wy - self.wy
                b = Bullet(self.wx, self.wy, dx, dy, 10.0, self.damage, 0, (100, 255, 100), self.player.uid)
                bullet_list.append(b)

    def draw(self, surf, cam):
        sx, sy = cam.world_to_screen(self.wx, self.wy)
        bob = math.sin(pygame.time.get_ticks() * 0.005) * 5
        pygame.draw.circle(surf, (100, 255, 100), (sx, sy - 20 - bob), 5 * cam.zoom)
        pygame.draw.line(surf, (50, 150, 50), (sx, sy - 20 - bob), (sx, sy), 1)

# --- PLAYER ---
class Player(Entity):
    def __init__(self):
        super().__init__(MAP_W/2, MAP_H/2)
        self.vx = 0
        self.vy = 0
        self.weapon_type = "pistol"
        self.grenade_count = PLAYER_START_GRENADES
        self.dash_cooldown = 0
        self.is_dashing = False
        self.dash_timer = 0
        self.ghost_spawn_timer = 0 # Timer for spawning traces
        self.money = 0
        self.stats = {
            "hp_max": PLAYER_START_HP,
            "hp_regen": 0.0,
            "speed": PLAYER_BASE_SPEED,
            "damage": 10.0,
            "fire_rate": 4.0,
            "bullet_speed": 12.0,
            "spread": 0.05,
            "pierce": 0,
            # NEW DASH STATS
            "dash_duration": 0.25, # Base duration
            "dash_speed_mult": 3.0 # Base speed multiplier
        }
        self.health = self.stats["hp_max"]
        self.last_shot = 0
        self.anim_timer = 0
        self.color_body = (60, 150, 255)
        self.drones = []

    def add_drone(self):
        self.drones.append(Drone(self, len(self.drones), len(self.drones)+1))
        count = len(self.drones)
        for i, d in enumerate(self.drones):
            d.total = count
            d.index = i
            d.angle_offset = (6.28 / count) * i

    def update(self, dt, enemies, bullets, grid, vm):
        self.physics_update(dt)
        if self.dash_cooldown > 0:
            self.dash_cooldown -= dt

        if self.is_dashing:
            self.dash_timer -= dt

            # GHOST SPAWN LOGIC
            self.ghost_spawn_timer -= dt
            if self.ghost_spawn_timer <= 0:
                vm.add_ghost(self.wx, self.wy, (100, 100, 255), 14)
                self.ghost_spawn_timer = 0.03 # Trace frequency

            if self.dash_timer <= 0:
                self.is_dashing = False
                self.vx /= self.stats["dash_speed_mult"]
                self.vy /= self.stats["dash_speed_mult"]

        step_x = self.vx * dt
        step_y = self.vy * dt
        self.check_wall_collision(step_x, step_y, grid)

        if self.health < self.stats["hp_max"] and self.stats["hp_regen"] > 0:
            self.health += self.stats["hp_regen"] * dt
            if self.health > self.stats["hp_max"]:
                self.health = self.stats["hp_max"]

        self.last_shot += dt
        self.anim_timer += dt * 5

        for d in self.drones:
            d.update(dt, enemies, bullets)

    def attempt_dash(self):
        if self.dash_cooldown <= 0 and not self.is_dashing:
            self.is_dashing = True
            # Use upgraded stats
            self.dash_timer = self.stats["dash_duration"]
            self.dash_cooldown = 1.2
            self.vx *= self.stats["dash_speed_mult"]
            self.vy *= self.stats["dash_speed_mult"]
            return True
        return False

    def shoot(self, target_wx, target_wy, vm):
        if self.last_shot < (1.0 / self.stats["fire_rate"]):
            return []

        cooldown_mod = 1.0
        recoil_force = 0.0

        if self.weapon_type == "shotgun":
            cooldown_mod = 1.5
            recoil_force = 3.0
        if self.weapon_type == "sniper":
            cooldown_mod = 2.5
            recoil_force = 6.0

        self.last_shot = 0 - (1.0/self.stats["fire_rate"]) * (cooldown_mod - 1.0)

        bullets = []
        dx = target_wx - self.wx
        dy = target_wy - self.wy
        base_angle = math.atan2(dy, dx)

        if recoil_force > 0:
            self.apply_knockback(-math.cos(base_angle) * recoil_force, -math.sin(base_angle) * recoil_force)

        if self.weapon_type == "shotgun":
            for _ in range(5):
                angle = base_angle + random.uniform(-0.3, 0.3)
                bx = math.cos(angle)
                by = math.sin(angle)
                spd = self.stats["bullet_speed"] * random.uniform(0.8, 1.1)
                dmg = self.stats["damage"] * 0.6
                b = Bullet(self.wx, self.wy, bx, by, spd, dmg, 0, (255, 100, 100), self.uid)
                b.lifetime = 0.6
                bullets.append(b)

        elif self.weapon_type == "sniper":
            bx = math.cos(base_angle)
            by = math.sin(base_angle)
            b = Bullet(self.wx, self.wy, bx, by, self.stats["bullet_speed"] * 2.0, self.stats["damage"] * 4.0, self.stats["pierce"] + 10, (100, 255, 255), self.uid)
            bullets.append(b)

        else: # Pistol
            angle = base_angle + random.uniform(-self.stats["spread"], self.stats["spread"])
            bx = math.cos(angle)
            by = math.sin(angle)
            b = Bullet(self.wx, self.wy, bx, by, self.stats["bullet_speed"], self.stats["damage"], int(self.stats["pierce"]), (255, 255, 150), self.uid)
            bullets.append(b)

        return bullets

    def draw(self, surf, cam):
        sx, sy = cam.world_to_screen(self.wx, self.wy)

        bob = math.sin(self.anim_timer) * 3
        center_y = sy - (15 * cam.zoom) + bob
        col = self.color_body
        if self.is_dashing: col = (200, 200, 255)
        pygame.draw.circle(surf, col, (sx, center_y), 14 * cam.zoom)
        if self.weapon_type == "shotgun":
            pygame.draw.circle(surf, (255, 50, 50), (sx + 10*cam.zoom, center_y), 5*cam.zoom)
        elif self.weapon_type == "sniper":
             pygame.draw.line(surf, (50, 255, 50), (sx, center_y), (sx+15*cam.zoom, center_y), int(3*cam.zoom))
        pygame.draw.circle(surf, (150, 200, 255), (sx - 4*cam.zoom, center_y - 4*cam.zoom), 5*cam.zoom)
        for d in self.drones:
            d.draw(surf, cam)
        w = 40 * cam.zoom
        h = 6 * cam.zoom
        bar_x = sx - w//2
        bar_y = sy - 40 * cam.zoom
        pygame.draw.rect(surf, (20,20,20), (bar_x, bar_y, w, h))
        pct = clamp(self.health / self.stats["hp_max"], 0, 1)
        pygame.draw.rect(surf, (50, 255, 50), (bar_x+1, bar_y+1, int((w-2)*pct), h-2))