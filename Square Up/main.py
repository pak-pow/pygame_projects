# main.py
"""
ISOMETRIC SHOOTER - TITAN EDITION (EXPANDED v7.5)
================================================================================
UPDATED: December 8, 2025
CHANGELOG:
- Fixed Recoil Wall Glitch
- New Cinematic Intro (Smoother, no trail)
- Added Ultimate System (Key Q) & Energy Orbs
"""

import math
import random
import pygame
from pygame.locals import *

# Module Imports
from config import *
from utils import check_grid_collision, distance, clamp
from camera import Camera
from visuals import VisualManager
from entities import Player, Grenade, HexBoss, SpikeEnemy, BlockEnemy, OrbEnemy, EnergyOrb
from map_gen import generate_map, create_wall_entities, draw_floor_grid
from ui import Button


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Square Up - v7.5")

        self.clock = pygame.time.Clock()

        # --- FONTS ---
        self.font_ui = pygame.font.SysFont("Verdana", 14, bold=True)
        self.font_big = pygame.font.SysFont("Verdana", 24, bold=True)
        self.font_wave = pygame.font.SysFont("Verdana", 30, bold=True)
        self.font_enemy_count = pygame.font.SysFont("Verdana", 40, bold=True)
        self.intro_font = pygame.font.SysFont("Impact", 80)
        self.intro_sub_font = pygame.font.SysFont("Verdana", 30, bold=True)  # New Font
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
        self.orbs = []  # List for Energy Orbs

        self.wave_active = True
        self.enemies_spawned = 0
        self.enemies_killed_in_wave = 0
        self.enemies_to_spawn = 10
        self.spawn_timer = 0

        self.init_shop()
        self.game_over = False

        # --- CINEMATIC INTRO VARIABLES ---
        self.intro_active = True
        self.intro_z = 8000.0
        self.intro_vz = 0.0
        self.intro_phase = "FALL"
        self.intro_msg_offset = 100
        self.intro_cam_shake = 0

        # Smooth Text Animation Variables
        self.intro_text_x = 400.0
        self.intro_text_alpha = 0.0

    def init_shop(self):
        self.buttons = []
        w, h = 220, 50
        x1, y = 20, SCREEN_H - 240
        x2, x3, x4 = 250, 480, 710

        def up_dmg(p): p.stats["damage"] *= 1.2

        def cost_dmg(): return int(self.player.stats["damage"] * 15), f"Dmg: {self.player.stats['damage']:.1f}"

        def up_fr(p): p.stats["fire_rate"] += 0.5

        def cost_fr(): return int(self.player.stats["fire_rate"] * 40), f"Rate: {self.player.stats['fire_rate']:.1f}"

        def up_spd(p): p.stats["speed"] *= 1.05

        def cost_spd(): return int(self.player.stats["speed"] * 50), f"Spd: {self.player.stats['speed']:.1f}"

        def up_pierce(p): p.stats["pierce"] += 1

        def cost_pierce(): return int(200 * (self.player.stats["pierce"] + 1)), f"Pierce: {self.player.stats['pierce']}"

        def up_regen(p): p.stats["hp_regen"] += 0.5

        def cost_regen(): return int(
            100 * (self.player.stats["hp_regen"] + 1)), f"Regen: {self.player.stats['hp_regen']:.1f}"

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

        def up_dash(p):
            p.stats["dash_duration"] += 0.05
            p.stats["dash_speed_mult"] += 0.2

        def cost_dash(): return int(
            300 * (self.player.stats["dash_duration"] * 10)), f"Dash: {self.player.stats['dash_duration']:.2f}s"

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
        self.orbs = []  # Clear orbs between levels

        self.map_grid = generate_map(MAP_W, MAP_H, self.level)
        self.walls = create_wall_entities(self.map_grid, self.level)

        margin = self.player.radius
        if self.player.check_area_collision(self.player.wx - margin, self.player.wx + margin, self.player.wy - margin,
                                            self.player.wy + margin, self.map_grid):
            px, py = int(self.player.wx), int(self.player.wy)
            found_safe = False
            for r in range(1, 10):
                for dy in range(-r, r + 1):
                    for dx in range(-r, r + 1):
                        if abs(dx) != r and abs(dy) != r: continue
                        tx, ty = px + dx, py + dy
                        if 0 <= tx < MAP_W and 0 <= ty < MAP_H and self.map_grid[ty][tx] == 0:
                            self.player.wx, self.player.wy = tx + 0.5, ty + 0.5
                            found_safe = True
                            break
                    if found_safe: break
                if found_safe: break
            if not found_safe: self.player.wx, self.player.wy = MAP_W / 2, MAP_H / 2

        self.vm.add_text(SCREEN_W / 2, SCREEN_H / 2 - 100, f"LEVEL {self.level} STARTED", (255, 255, 100), 2.0, size=30)
        self.cam.add_shake(10)

    def spawn_enemy(self):
        attempts = 0
        while attempts < 20:
            ix, iy = random.randint(1, MAP_W - 2), random.randint(1, MAP_H - 2)
            if self.map_grid[iy][ix] == 0:
                wx, wy = ix + 0.5, iy + 0.5
                if distance(wx, wy, self.player.wx, self.player.wy) < 5.0:
                    attempts += 1;
                    continue

                r = random.random()
                e = None
                if self.level % 5 == 0 and self.enemies_spawned == self.enemies_to_spawn - 1:
                    e = HexBoss(wx, wy, self.level, self.vm)
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
            if distance(gx, gy, e.wx, e.wy) < radius_world:
                e.take_damage(damage)

    def draw_vignette(self):
        if self.intro_active: return
        self.fog.fill((10, 10, 20))
        px, py = self.cam.world_to_screen(self.player.wx + 0.5, self.player.wy + 0.5)
        pygame.draw.circle(self.fog, (255, 255, 255), (px, py), 300 * self.cam.zoom)
        self.fog.set_colorkey((255, 255, 255))
        self.fog.set_alpha(150)
        self.screen.blit(self.fog, (0, 0))

    # --- UI / HUD (BROTATO STYLE) ---
    def draw_hud(self):
        if self.intro_active: return

        # 1. HEALTH BAR
        bar_w, bar_h = 200, 25
        bar_x, bar_y = 20, 20
        pygame.draw.rect(self.screen, (30, 30, 30), (bar_x, bar_y, bar_w, bar_h))
        pct = clamp(self.player.health / self.player.stats["hp_max"], 0, 1)
        pygame.draw.rect(self.screen, (200, 50, 50), (bar_x + 2, bar_y + 2, (bar_w - 4) * pct, bar_h - 4))
        hp_text = f"{int(self.player.health)} / {int(self.player.stats['hp_max'])}"
        txt_surf = self.font_ui.render(hp_text, True, (255, 255, 255))
        self.screen.blit(txt_surf, (bar_x + bar_w // 2 - txt_surf.get_width() // 2, bar_y + 4))

        # 2. ULTIMATE GAUGE (FIX 4)
        ult_w, ult_h = 200, 15
        ult_y = bar_y + bar_h + 2
        pygame.draw.rect(self.screen, (20, 20, 40), (bar_x, ult_y, ult_w, ult_h))

        # Color based on readiness
        ult_pct = clamp(self.player.energy / self.player.max_energy, 0, 1)
        u_col = (100, 100, 100)  # Gray if empty
        if self.player.ultimate_active:
            u_col = (0, 255, 255)  # Cyan if active
            ult_pct = self.player.ultimate_timer / self.player.ultimate_duration
        elif self.player.energy >= self.player.max_energy:
            u_col = (255, 255, 0)  # Gold if ready

        pygame.draw.rect(self.screen, u_col, (bar_x + 1, ult_y + 1, (ult_w - 2) * ult_pct, ult_h - 2))

        msg = "Q: ULTIMATE"
        if self.player.ultimate_active:
            msg = "ACTIVE!"
        elif self.player.energy < self.player.max_energy:
            msg = f"{int(self.player.energy)}%"

        u_txt = self.font_ui.render(msg, True, (0, 0, 0))
        self.screen.blit(u_txt, (bar_x + ult_w // 2 - u_txt.get_width() // 2, ult_y - 2))

        # 3. LEVEL
        lvl_w, lvl_h = 100, 15
        lvl_y = ult_y + ult_h + 5
        pygame.draw.rect(self.screen, (30, 30, 30), (bar_x, lvl_y, lvl_w, lvl_h))
        pygame.draw.rect(self.screen, (50, 200, 50), (bar_x + 2, lvl_y + 2, lvl_w - 4, lvl_h - 4))
        lvl_txt = self.font_ui.render(f"LV. {self.level}", True, (255, 255, 255))
        self.screen.blit(lvl_txt, (bar_x + 5, lvl_y - 2))

        # 4. COINS
        coin_y = lvl_y + lvl_h + 10
        pygame.draw.circle(self.screen, COL_MONEY, (bar_x + 10, coin_y + 10), 10)
        money_txt = self.font_big.render(f"{int(self.player.money)}", True, COL_MONEY)
        self.screen.blit(money_txt, (bar_x + 25, coin_y))

        # 5. WAVE COUNTER
        cx = SCREEN_W // 2
        wave_txt = self.font_wave.render(f"WAVE {self.level}", True, (255, 255, 255))
        self.screen.blit(wave_txt, (cx - wave_txt.get_width() // 2, 20))

        # 6. ENEMY COUNT
        remaining_real = (self.enemies_to_spawn - self.enemies_spawned) + len(self.enemies)
        if not self.wave_active: remaining_real = 0
        enemy_txt = self.font_enemy_count.render(f"{remaining_real}", True, (255, 50, 50))
        self.screen.blit(enemy_txt, (cx - enemy_txt.get_width() // 2, 55))

        # 7. DASH COOLDOWN
        dash_x = bar_x + bar_w + 10
        dash_y = bar_y
        dash_size = 30
        pygame.draw.rect(self.screen, (50, 50, 50), (dash_x, dash_y, dash_size, dash_size))
        pygame.draw.rect(self.screen, (200, 200, 200), (dash_x, dash_y, dash_size, dash_size), 2)
        boot_col = (100, 200, 255)
        if self.player.dash_cooldown > 0: boot_col = (100, 100, 100)
        pygame.draw.rect(self.screen, boot_col, (dash_x + 5, dash_y + 10, 20, 15))  # Foot
        pygame.draw.rect(self.screen, boot_col, (dash_x + 5, dash_y + 5, 8, 10))  # Leg

        if self.player.dash_cooldown > 0:
            max_cd = 1.2
            ratio = self.player.dash_cooldown / max_cd
            fill_h = int(dash_size * ratio)
            s = pygame.Surface((dash_size, fill_h))
            s.set_alpha(150)
            s.fill((0, 0, 0))
            self.screen.blit(s, (dash_x, dash_y + (dash_size - fill_h)))

        # Shop Overlay
        if not self.wave_active:
            overlay = pygame.Surface((SCREEN_W, 250))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(180)
            self.screen.blit(overlay, (0, SCREEN_H - 250))
            msg = self.shop_font.render("SHOP OPEN - Press ENTER", True, (100, 255, 100))
            self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H - 290))

            for b in self.buttons: b.draw(self.screen, self.font_ui, self.player.money)

    def draw_game_over(self):
        self.screen.fill((20, 0, 0))
        # Fixed typo: self.title_font was not defined, switched to intro_font
        txt = self.intro_font.render("GAME OVER", True, (255, 50, 50))
        restart = self.font_big.render("Press R to Restart", True, (255, 255, 255))
        cx, cy = SCREEN_W // 2, SCREEN_H // 2
        self.screen.blit(txt, (cx - txt.get_width() // 2, cy - 50))
        self.screen.blit(restart, (cx - restart.get_width() // 2, cy + 50))
        pygame.display.flip()

    # --- FIX 2: IMPROVED CINEMATIC RENDERER ---
    def draw_intro(self):
        self.screen.fill((10, 10, 15))
        cx, cy = SCREEN_W // 2, SCREEN_H // 2

        shake_x = random.randint(-self.intro_cam_shake, self.intro_cam_shake)
        shake_y = random.randint(-self.intro_cam_shake, self.intro_cam_shake)
        cx += shake_x
        cy += shake_y

        # Speed Tunnel (Refined)
        loop_h = SCREEN_H
        scroll_y = (pygame.time.get_ticks() * 2.0) % loop_h
        for i in range(20):
            rx = (i * 137) % SCREEN_W
            ry = (scroll_y + (i * 200)) % loop_h
            dist_from_center = abs(rx - SCREEN_W // 2) / (SCREEN_W // 2)
            line_len = 50 + int(100 * dist_from_center)
            # Fainter lines
            col_line = (30, 30, 60)
            pygame.draw.line(self.screen, col_line, (rx, ry), (rx, ry - line_len), 2)

        # Draw Ground coming up
        ground_threshold = 2000.0
        if self.intro_z < ground_threshold:
            alpha_ground = 1.0 - (self.intro_z / ground_threshold)
            ground_y_offset = (self.intro_z * 1.5)
            rect_w = 400 * (1.0 + alpha_ground)
            rect_h = 200 * (1.0 + alpha_ground)
            g_rect = pygame.Rect(0, 0, rect_w, rect_h)
            g_rect.center = (cx, cy + ground_y_offset)
            pygame.draw.rect(self.screen, (30, 30, 50), g_rect)
            pygame.draw.rect(self.screen, (100, 100, 150), g_rect, 2)

        # Player Ball (Glow effect, no ugly tail)
        ball_x = cx
        ball_y = cy

        # Subtle drift
        ball_x += math.sin(pygame.time.get_ticks() * 0.01) * 10

        # Glow
        for i in range(3):
            r = 25 + i * 5
            s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (60, 150, 255, 50), (r, r), r)
            self.screen.blit(s, (ball_x - r, ball_y - r))

        pygame.draw.circle(self.screen, self.player.color_body, (ball_x, ball_y), 20)
        pygame.draw.circle(self.screen, (150, 200, 255), (ball_x - 6, ball_y - 6), 8)

        # FIX 2: ANIMATED TEXT LOGIC
        # Thresholds for text appearing based on Z distance

        # "SURVIVE" enters
        if self.intro_z < 6000:
            txt = self.intro_font.render("SURVIVE", True, (255, 255, 255))
            txt.set_alpha(int(self.intro_text_alpha))

            # Text moves from right to left next to ball
            txt_x = ball_x + 60 + self.intro_text_x
            txt_y = ball_y - 40
            self.screen.blit(txt, (txt_x, txt_y))

        # "UNTIL YOU CAN" delayed appearance
        if self.intro_z < 3500:
            # Subtle fade in
            sub_alpha = min(255, (3500 - self.intro_z) * 0.2)
            sub_txt = self.intro_sub_font.render("[ UNTIL YOU CAN ]", True, (200, 50, 50))
            sub_txt.set_alpha(int(sub_alpha))

            sub_x = ball_x + 60 + self.intro_text_x + 10
            sub_y = ball_y + 45  # Below Survive
            self.screen.blit(sub_txt, (sub_x, sub_y))

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
                    if event.key == K_SPACE: self.cam.rotate_view()
                    if event.key == K_RETURN and not self.wave_active: self.start_next_level()
                    if event.key == K_r and self.game_over: self.reset_game()
                    # ULTIMATE KEY
                    if event.key == K_q:
                        if self.player.activate_ultimate():
                            self.vm.add_text(SCREEN_W // 2, SCREEN_H // 2 - 200, "ULTIMATE ACTIVATED!", (0, 255, 255),
                                             2.0, 30)
                            self.cam.add_shake(20)

                elif event.type == MOUSEBUTTONDOWN:
                    if not self.intro_active and not self.game_over and event.button == 1:
                        if not self.wave_active:
                            for b in self.buttons: b.click(mx, my, self.player)
                    elif not self.intro_active and event.button == 3:
                        if self.player.grenade_count > 0:
                            m_wx, m_wy = self.cam.screen_to_world(mx, my)
                            self.grenades.append(Grenade(self.player.wx, self.player.wy, m_wx, m_wy))
                            self.player.grenade_count -= 1

            if self.game_over:
                self.draw_game_over()
                continue

            # --- INTRO LOGIC ---
            if self.intro_active:
                self.intro_vz += 2000.0 * dt
                self.intro_z -= self.intro_vz * dt
                self.intro_cam_shake = int(self.intro_vz / 500.0)

                # Smooth Text Animation
                if self.intro_z < 6000:
                    self.intro_text_x += (0 - self.intro_text_x) * 3.0 * dt
                    self.intro_text_alpha = min(255, self.intro_text_alpha + 300 * dt)

                if self.intro_z <= 0:
                    self.intro_z = 0
                    self.intro_active = False
                    self.cam.add_shake(60)
                    sx, sy = self.cam.world_to_screen(self.player.wx, self.player.wy)
                    for _ in range(10): self.vm.add_crack(self.player.wx, self.player.wy, (200, 200, 200))
                    self.vm.add_explosion(sx, sy, (255, 255, 255))
                    self.vm.add_text(sx, sy - 100, "BEGIN!", (255, 50, 50), 2.0, 30)

                self.draw_intro()
                pygame.display.flip()
                continue

                # --- NORMAL GAMEPLAY ---
            keys = pygame.key.get_pressed()
            if keys[K_LSHIFT]: self.player.attempt_dash()
            input_x, input_y = 0, 0
            if keys[K_w] or keys[K_UP]: input_y = -1
            if keys[K_s] or keys[K_DOWN]: input_y = 1
            if keys[K_a] or keys[K_LEFT]: input_x = -1
            if keys[K_d] or keys[K_RIGHT]: input_x = 1

            idx = self.cam.rotation_index % 4
            vx, vy = 0, 0
            if idx == 0:
                vx, vy = input_x, input_y
            elif idx == 1:
                vx, vy = input_y, -input_x
            elif idx == 2:
                vx, vy = -input_x, -input_y
            elif idx == 3:
                vx, vy = -input_y, input_x

            if vx != 0 or vy != 0:
                l = math.hypot(vx, vy)
                vx /= l
                vy /= l
                speed = self.player.stats["speed"]
                if self.player.is_dashing: speed *= 3.0
                self.player.vx = vx * speed
                self.player.vy = vy * speed
            else:
                if not self.player.is_dashing: self.player.vx, self.player.vy = 0, 0

            self.player.update(dt, self.enemies, self.bullets, self.map_grid, self.vm)

            # Collecting Orbs
            for orb in self.orbs:
                orb.update(dt)
                if distance(self.player.wx, self.player.wy, orb.wx, orb.wy) < 1.0:
                    orb.lifetime = 0
                    self.player.energy = min(self.player.max_energy, self.player.energy + 10)
                    # Visual feedback
                    sx, sy = self.cam.world_to_screen(orb.wx, orb.wy)
                    self.vm.add_particle(sx, sy, (0, 255, 255))
            self.orbs = [o for o in self.orbs if o.lifetime > 0]

            if pygame.mouse.get_pressed()[0]:
                if self.wave_active or (my < SCREEN_H - 250):
                    m_wx, m_wy = self.cam.screen_to_world(mx, my)
                    new_bullets = self.player.shoot(m_wx, m_wy, self.vm)
                    if new_bullets:
                        self.bullets.extend(new_bullets)
                        if not self.player.ultimate_active:  # Don't spawn casing spam during ult
                            self.vm.add_casing(self.player.wx, self.player.wy)

            self.cam.set_target(self.player.wx, self.player.wy)
            self.cam.update(dt)

            if self.wave_active:
                if self.enemies_spawned < self.enemies_to_spawn:
                    self.spawn_timer -= dt
                    if self.spawn_timer <= 0:
                        self.spawn_enemy()
                        self.spawn_timer = max(0.5, 2.0 - self.level * 0.1)
                elif len(self.enemies) == 0:
                    self.wave_active = False
                    self.player.money += 50 * self.level

            for b in self.bullets: b.update(dt)
            self.bullets = [b for b in self.bullets if b.lifetime > 0]
            for g in self.grenades:
                g.update(dt, self.map_grid)
                if g.exploded: self.handle_explosion(g.x, g.y, 80.0, 4.0)
            self.grenades = [g for g in self.grenades if not g.exploded]

            for e in self.enemies:
                e.update(dt, self.player, self.map_grid)
                if not self.player.is_dashing:
                    if distance(self.player.wx, self.player.wy, e.wx, e.wy) < 0.8:
                        self.player.health -= e.damage_to_player * dt
                        self.damage_alpha = 150.0

            if self.player.health <= 0:
                self.game_over = True
                sx, sy = self.cam.world_to_screen(self.player.wx, self.player.wy)
                self.vm.add_explosion(sx, sy, (255, 0, 0))

            for b in self.bullets:
                if check_grid_collision(b.wx, b.wy, self.map_grid):
                    b.lifetime = 0
                    sx, sy = self.cam.world_to_screen(b.wx, b.wy)
                    self.vm.add_particle(sx, sy, (200, 200, 200))
                for e in self.enemies:
                    if e.uid in b.hit_list: continue
                    if distance(e.wx, e.wy, b.wx, b.wy) < 0.8:
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
                    for _ in range(8): self.vm.add_particle(sx, sy, e.color)

                    # FIX 3: Spawn Energy Orb Chance (50%)
                    if random.random() < 1:
                        self.orbs.append(EnergyOrb(e.wx, e.wy))
                else:
                    survivors.append(e)
            self.enemies = survivors

            self.vm.update(dt)

            self.screen.fill(COL_BG)
            draw_floor_grid(self.screen, self.cam, MAP_W, MAP_H, self.level)
            self.vm.draw_floor(self.screen, self.cam)
            self.vm.draw_ghosts(self.screen, self.cam)

            # Draw Orbs
            for orb in self.orbs: orb.draw(self.screen, self.cam)

            render_list = []
            render_list.append(self.player)
            render_list.extend(self.enemies)
            render_list.extend(self.walls)
            render_list.sort(key=lambda x: self.cam.world_to_screen(x.wx, x.wy)[1])

            for entity in render_list: entity.draw(self.screen, self.cam)

            for b in self.bullets: b.draw(self.screen, self.cam)
            for g in self.grenades: g.draw(self.screen, self.cam)

            self.vm.draw_top(self.screen, self.cam)
            self.draw_vignette()

            if self.damage_alpha > 0:
                flash_surf = pygame.Surface((SCREEN_W, SCREEN_H))
                flash_surf.fill((255, 0, 0))
                flash_surf.set_alpha(int(self.damage_alpha))
                self.screen.blit(flash_surf, (0, 0))
                self.damage_alpha = max(0, self.damage_alpha - 300 * dt)

            self.draw_hud()
            pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    Game().run()