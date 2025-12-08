# main.py
"""
ISOMETRIC SHOOTER - TITAN EDITION (EXPANDED v6.0)
================================================================================
CREATED FOR: Paul
DATE: December 7, 2025
VERSION: 6.0 (Full Expanded Formatting)
"""

import math
import random
import pygame
from pygame.locals import *

# Module Imports
from config import *
from utils import check_grid_collision, distance
from camera import Camera
from visuals import VisualManager
from entities import Player, Grenade, HexBoss, SpikeEnemy, BlockEnemy, OrbEnemy
from map_gen import generate_map, create_wall_entities, draw_floor_grid
from ui import Button

# ==========================================
# MAIN GAME LOGIC
# ==========================================
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Isometric Titan Shooter - v6.0 Dash Update")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("Consolas", 16, bold=True)
        self.title_font = pygame.font.SysFont("Verdana", 60, bold=True)
        self.shop_font = pygame.font.SysFont("Verdana", 30, bold=True)

        self.fog = pygame.Surface((SCREEN_W, SCREEN_H))
        self.damage_alpha = 0.0

        self.reset_game()

    def reset_game(self):
        self.level = 1
        self.player = Player()
        self.cam = Camera(SCREEN_W, SCREEN_H)
        self.cam.set_target(self.player.wx, self.player.wy)
        self.cam.focus_wx = self.player.wx
        self.cam.focus_wy = self.player.wy

        self.vm = VisualManager()
        self.map_grid = generate_map(MAP_W, MAP_H, self.level)
        self.walls = create_wall_entities(self.map_grid, self.level)

        self.bullets = []
        self.enemies = []
        self.grenades = []

        self.wave_active = True
        self.enemies_spawned = 0
        self.enemies_killed_in_wave = 0
        self.enemies_to_spawn = 10
        self.spawn_timer = 0

        self.init_shop()
        self.game_over = False

    def init_shop(self):
        self.buttons = []
        w, h = 220, 50
        x1 = 20
        x2 = 250
        x3 = 480
        x4 = 710
        y = SCREEN_H - 240

        def up_dmg(p): p.stats["damage"] *= 1.2
        def cost_dmg(): return int(self.player.stats["damage"] * 15), f"Dmg: {self.player.stats['damage']:.1f}"

        def up_fr(p): p.stats["fire_rate"] += 0.5
        def cost_fr(): return int(self.player.stats["fire_rate"] * 40), f"Rate: {self.player.stats['fire_rate']:.1f}"

        def up_spd(p): p.stats["speed"] *= 1.05
        def cost_spd(): return int(self.player.stats["speed"] * 50), f"Spd: {self.player.stats['speed']:.1f}"

        def up_pierce(p): p.stats["pierce"] += 1
        def cost_pierce(): return int(200 * (self.player.stats["pierce"] + 1)), f"Pierce: {self.player.stats['pierce']}"

        def up_regen(p): p.stats["hp_regen"] += 0.5
        def cost_regen(): return int(100 * (self.player.stats["hp_regen"] + 1)), f"Regen: {self.player.stats['hp_regen']:.1f}"

        def heal(p): p.health = min(p.health + 30, p.stats["hp_max"])
        def cost_heal(): return 20, f"HP: {int(self.player.health)}"

        def buy_shotgun(p): p.weapon_type = "shotgun"
        def cost_shotgun(): return 500, "Spread Shot"

        def buy_sniper(p): p.weapon_type = "sniper"
        def cost_sniper(): return 800, "Pierce Shot"

        def buy_drone(p): p.add_drone()
        def cost_drone(): return 300 * (len(self.player.drones) + 1), f"Count: {len(self.player.drones)}"

        def buy_nade(p): p.grenade_count += 3
        def cost_nade(): return 100, f"Nades: {self.player.grenade_count}"

        # NEW DASH UPGRADE
        def up_dash(p):
            p.stats["dash_duration"] += 0.05
            p.stats["dash_speed_mult"] += 0.2
        def cost_dash(): return int(300 * (self.player.stats["dash_duration"] * 10)), f"Dash: {self.player.stats['dash_duration']:.2f}s"

        self.buttons.append(Button((x1, y, w, h), "Damage +20%", up_dmg, cost_dmg))
        self.buttons.append(Button((x1, y + 60, w, h), "Fire Rate +0.5", up_fr, cost_fr))
        self.buttons.append(Button((x1, y + 120, w, h), "Speed +5%", up_spd, cost_spd))

        self.buttons.append(Button((x2, y, w, h), "Pierce +1", up_pierce, cost_pierce))
        self.buttons.append(Button((x2, y + 60, w, h), "Regen +0.5", up_regen, cost_regen))
        self.buttons.append(Button((x2, y + 120, w, h), "Heal (30HP)", heal, cost_heal))

        self.buttons.append(Button((x3, y, w, h), "BUY SHOTGUN", buy_shotgun, cost_shotgun))
        self.buttons.append(Button((x3, y + 60, w, h), "BUY SNIPER", buy_sniper, cost_sniper))
        self.buttons.append(Button((x3, y + 120, w, h), "UPGRADE DASH", up_dash, cost_dash))

        self.buttons.append(Button((x4, y, w, h), "BUY DRONE", buy_drone, cost_drone))
        self.buttons.append(Button((x4, y + 60, w, h), "BUY GRENADES x3", buy_nade, cost_nade))

    def start_next_level(self):
        self.level += 1
        self.wave_active = True
        self.enemies_spawned = 0
        self.enemies_killed_in_wave = 0
        self.enemies_to_spawn = 10 + int(self.level * 2.5)
        self.map_grid = generate_map(MAP_W, MAP_H, self.level)
        self.walls = create_wall_entities(self.map_grid, self.level)
        self.vm.add_text(SCREEN_W / 2, SCREEN_H / 2 - 100, f"LEVEL {self.level} STARTED", (255, 255, 100), 2.0, size=30)
        self.cam.add_shake(10)

    def spawn_enemy(self):
        attempts = 0
        while attempts < 20:
            if random.choice([True, False]):
                wx = random.choice([0, MAP_W-1])
                wy = random.uniform(0, MAP_H)
            else:
                wx = random.uniform(0, MAP_W)
                wy = random.choice([0, MAP_H-1])

            if not check_grid_collision(wx, wy, self.map_grid):
                r = random.random()
                e = None
                if self.level % 5 == 0 and self.enemies_spawned == self.enemies_to_spawn - 1:
                     e = HexBoss(wx, wy, self.level, self.vm)
                     self.vm.add_text(SCREEN_W/2, SCREEN_H/2, "BOSS DETECTED", (255,50,50), 3.0, 30)
                elif r < 0.2 and self.level > 2:
                    e = SpikeEnemy(wx, wy, self.level, self.vm)
                elif r < 0.4 and self.level > 1:
                    e = BlockEnemy(wx, wy, self.level, self.vm)
                else:
                    e = OrbEnemy(wx, wy, self.level, self.vm)

                self.enemies.append(e)
                self.enemies_spawned += 1
                return
            attempts += 1

    def handle_explosion(self, gx, gy, damage, radius_world):
        self.cam.add_shake(15)
        sx, sy = self.cam.world_to_screen(gx, gy)
        self.vm.add_explosion(sx, sy)

        for e in self.enemies:
            dist = distance(gx, gy, e.wx, e.wy)
            if dist < radius_world:
                dmg = damage * (1.0 - (dist / radius_world) * 0.5)
                e.take_damage(dmg)
                angle = math.atan2(e.wy - gy, e.wx - gx)
                force = 20.0 * (1.0 - dist/radius_world)
                e.apply_knockback(math.cos(angle)*force, math.sin(angle)*force)
                esx, esy = self.cam.world_to_screen(e.wx, e.wy)
                self.vm.add_text(esx, esy - 50, f"{int(dmg)}!", COL_EXPLOSION, 1.0, 20)

    def draw_vignette(self):
        self.fog.fill((10, 10, 20))
        px, py = self.cam.world_to_screen(self.player.wx + 0.5, self.player.wy + 0.5)

        pygame.draw.circle(self.fog, (255, 255, 255), (px, py), 300 * self.cam.zoom)

        for b in self.bullets:
             bx, by = self.cam.world_to_screen(b.wx, b.wy)
             pygame.draw.circle(self.fog, (255,255,255), (bx, by), 30 * self.cam.zoom)

        for g in self.grenades:
            if g.timer < 0.5:
                gx, gy = self.cam.world_to_screen(g.x, g.y)
                pygame.draw.circle(self.fog, (255,200,200), (gx, gy), 100 * self.cam.zoom)

        self.fog.set_colorkey((255, 255, 255))
        self.fog.set_alpha(150)
        self.screen.blit(self.fog, (0, 0))

        # 1. UPDATE draw_hud TO SHOW NEW CONTROLS
    def draw_hud(self):
            infos = [
                f"Level: {self.level}",
                f"Wave Progress: {self.enemies_killed_in_wave} / {self.enemies_to_spawn}",
                f"Money: ${int(self.player.money)}",
                f"Weapon: {self.player.weapon_type.upper()}",
                f"Grenades: {self.player.grenade_count}",
                f"Drones: {len(self.player.drones)}"
            ]

            for i, text in enumerate(infos):
                surf = self.font.render(text, True, COL_TEXT)
                shadow = self.font.render(text, True, (0, 0, 0))
                self.screen.blit(shadow, (11, 11 + i * 25))
                self.screen.blit(surf, (10, 10 + i * 25))

            # UPDATED HINT TEXT
            hint = "Scroll: Zoom | Shift: Dash | SPACE: Rotate View | ENTER: Next Wave"
            hint_surf = self.font.render(hint, True, (150, 150, 150))
            self.screen.blit(hint_surf, (SCREEN_W - hint_surf.get_width() - 10, 10))

            if not self.wave_active:
                overlay = pygame.Surface((SCREEN_W, 250))
                overlay.fill((0, 0, 0))
                overlay.set_alpha(180)
                self.screen.blit(overlay, (0, SCREEN_H - 250))

                # UPDATED SHOP TEXT
                msg = self.shop_font.render("SHOP OPEN - Press ENTER for Next Wave", True, (100, 255, 100))
                self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H - 290))

                for b in self.buttons:
                    b.draw(self.screen, self.font, self.player.money)

    def draw_game_over(self):
        self.screen.fill((20, 0, 0))
        txt = self.title_font.render("GAME OVER", True, (255, 50, 50))
        sub = self.font.render(f"You reached Level {self.level}", True, (200, 200, 200))
        restart = self.font.render("Press R to Restart", True, (255, 255, 255))
        cx, cy = SCREEN_W//2, SCREEN_H//2
        self.screen.blit(txt, (cx - txt.get_width()//2, cy - 50))
        self.screen.blit(sub, (cx - sub.get_width()//2, cy + 10))
        self.screen.blit(restart, (cx - restart.get_width()//2, cy + 50))
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            dt_ms = self.clock.tick(FPS)
            dt = dt_ms / 1000.0
            mx, my = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEWHEEL:
                    if event.y > 0: self.cam.zoom_in()
                    if event.y < 0: self.cam.zoom_out()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE: running = False

                    # CHANGED: SPACE ROTATES CAMERA
                    if event.key == K_SPACE:
                        self.cam.rotate_view()

                    # CHANGED: ENTER STARTS NEXT LEVEL
                    if event.key == K_RETURN and not self.wave_active and not self.game_over:
                        self.start_next_level()

                    if event.key == K_r and self.game_over:
                        self.reset_game()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if not self.wave_active and not self.game_over:
                            for b in self.buttons:
                                b.click(mx, my, self.player)
                    elif event.button == 3:
                        if self.player.grenade_count > 0 and not self.game_over:
                            m_wx, m_wy = self.cam.screen_to_world(mx, my)
                            g = Grenade(self.player.wx, self.player.wy, m_wx, m_wy)
                            self.grenades.append(g)
                            self.player.grenade_count -= 1

            if self.game_over:
                self.draw_game_over()
                continue

            # MOVEMENT INPUT - ADJUSTED FOR ROTATION
            keys = pygame.key.get_pressed()
            if keys[K_LSHIFT]: self.player.attempt_dash()

            raw_vx = 0
            raw_vy = 0
            if keys[K_w] or keys[K_UP]: raw_vy = -1
            if keys[K_s] or keys[K_DOWN]: raw_vy = 1
            if keys[K_a] or keys[K_LEFT]: raw_vx = -1
            if keys[K_d] or keys[K_RIGHT]: raw_vx = 1

            # FIX: Apply INVERSE Rotation so controls stay relative to the SCREEN
            # If the camera rotates +Angle, we rotate inputs -Angle to compensate.
            c = math.cos(self.cam.angle)
            s = math.sin(self.cam.angle)

            # Inverse Rotation Formula:
            # new_x = x * cos + y * sin
            # new_y = -x * sin + y * cos
            vx = raw_vx * c + raw_vy * s
            vy = -raw_vx * s + raw_vy * c

            if vx != 0 or vy != 0:
                l = math.hypot(vx, vy)
                vx /= l
                speed = self.player.stats["speed"]
                if self.player.is_dashing:
                    speed *= 3.0
                self.player.vx = vx * speed
                self.player.vy = vy * speed
            else:
                if not self.player.is_dashing:
                    self.player.vx = 0
                    self.player.vy = 0

            # Pass VM to update to spawn ghosts
            self.player.update(dt, self.enemies, self.bullets, self.map_grid, self.vm)

            if pygame.mouse.get_pressed()[0]:
                if self.wave_active or (my < SCREEN_H - 250):
                    m_wx, m_wy = self.cam.screen_to_world(mx, my)
                    new_bullets = self.player.shoot(m_wx, m_wy, self.vm)
                    if new_bullets:
                        self.bullets.extend(new_bullets)
                        self.vm.add_casing(self.player.wx, self.player.wy)

            self.cam.set_target(self.player.wx, self.player.wy)
            self.cam.update(dt)

            if self.wave_active:
                if self.enemies_spawned < self.enemies_to_spawn:
                    self.spawn_timer -= dt
                    rate = max(0.5, 2.0 - self.level * 0.1)
                    if self.spawn_timer <= 0:
                        self.spawn_enemy()
                        self.spawn_timer = rate
                elif len(self.enemies) == 0:
                    self.wave_active = False
                    self.vm.add_text(SCREEN_W/2, SCREEN_H/2, "WAVE CLEARED", (100, 255, 100), 3.0, 30)
                    self.player.money += 50 * self.level

            for b in self.bullets: b.update(dt)
            self.bullets = [b for b in self.bullets if b.lifetime > 0]

            for g in self.grenades:
                g.update(dt, self.map_grid)
                if g.exploded:
                    self.handle_explosion(g.x, g.y, 80.0, 4.0)
            self.grenades = [g for g in self.grenades if not g.exploded]

            for e in self.enemies:
                e.update(dt, self.player, self.map_grid)
                if not self.player.is_dashing:
                    dx = self.player.wx - e.wx
                    dy = self.player.wy - e.wy
                    dist = math.hypot(dx, dy)
                    if dist < 0.8:
                        self.player.health -= e.damage_to_player * dt
                        self.damage_alpha = 150.0

            if self.player.health <= 0:
                self.game_over = True
                sx, sy = self.cam.world_to_screen(self.player.wx, self.player.wy)
                self.vm.add_explosion(sx, sy, (255,0,0))

            for b in self.bullets:
                if check_grid_collision(b.wx, b.wy, self.map_grid):
                    b.lifetime = 0
                    sx, sy = self.cam.world_to_screen(b.wx, b.wy)
                    self.vm.add_particle(sx, sy, (200,200,200))
                for e in self.enemies:
                    if e.uid in b.hit_list: continue
                    dx = e.wx - b.wx
                    dy = e.wy - b.wy
                    if math.hypot(dx, dy) < 0.8:
                        e.take_damage(b.damage)
                        b.hit_list.append(e.uid)
                        sx, sy = self.cam.world_to_screen(e.wx, e.wy)
                        self.vm.add_particle(sx, sy, e.color)
                        self.vm.add_text(sx, sy - 40, str(int(b.damage)), (255, 255, 255))
                        e.apply_knockback(b.vx * 0.2, b.vy * 0.2)
                        if b.pierce <= 0:
                            b.lifetime = 0
                            break
                        else:
                            b.pierce -= 1

            survivors = []
            for e in self.enemies:
                if e.dead:
                    self.player.money += e.money_value
                    self.enemies_killed_in_wave += 1
                    self.cam.add_shake(3.0)
                    sx, sy = self.cam.world_to_screen(e.wx, e.wy)
                    self.vm.add_text(sx, sy - 60, f"+${e.money_value}", COL_MONEY)
                    for _ in range(8):
                        self.vm.add_particle(sx, sy, e.color)
                else:
                    survivors.append(e)
            self.enemies = survivors

            self.vm.update(dt)

            self.screen.fill(COL_BG)
            draw_floor_grid(self.screen, self.cam, MAP_W, MAP_H, self.level)
            self.vm.draw_floor(self.screen, self.cam)
            self.vm.draw_ghosts(self.screen, self.cam) # Draw Dash Trails

            self.player.draw_shadow(self.screen, self.cam)
            for e in self.enemies:
                e.draw_shadow(self.screen, self.cam)

            render_list = []
            render_list.append(self.player)
            render_list.extend(self.enemies)
            render_list.extend(self.walls)

            render_list.sort(key=lambda x: self.cam.world_to_screen(x.wx, x.wy)[1])

            for entity in render_list:
                entity.draw(self.screen, self.cam)

            for b in self.bullets: b.draw(self.screen, self.cam)
            for g in self.grenades: g.draw(self.screen, self.cam)

            self.vm.draw_top(self.screen, self.cam)
            self.draw_vignette()

            if self.damage_alpha > 0:
                flash_surf = pygame.Surface((SCREEN_W, SCREEN_H))
                flash_surf.fill((255, 0, 0))
                flash_surf.set_alpha(int(self.damage_alpha))
                self.screen.blit(flash_surf, (0,0))
                self.damage_alpha = max(0, self.damage_alpha - 300 * dt)

            self.draw_hud()

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    Game().run()