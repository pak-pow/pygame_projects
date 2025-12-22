import pygame, sys, random

# 1. Setup
pygame.init()
SCREEN_W, SCREEN_H = 800, 600
display_surface = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()

# We draw everything to this 'wrapper' surface first, then shake THIS surface
world_surf = pygame.Surface((SCREEN_W, SCREEN_H))


# --- ADVANCED CLASSES ---

class ShakeManager:
    def __init__(self):
        self.trauma = 0.0
        self.shake_power = 20  # Max pixels to shake
        self.decay = 0.8  # How fast trauma falls per second

    def add_trauma(self, amount):
        self.trauma = min(self.trauma + amount, 1.0)  # Cap at 1.0

    def update(self, dt):
        if self.trauma > 0:
            self.trauma -= self.decay * dt
            if self.trauma < 0: self.trauma = 0

    def get_offset(self):
        # The Secret Sauce: Square the trauma
        intensity = self.trauma * self.trauma

        dx = (random.random() * 2 - 1) * self.shake_power * intensity
        dy = (random.random() * 2 - 1) * self.shake_power * intensity
        return int(dx), int(dy)


class GlowParticle(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__()
        self.pos = pygame.math.Vector2(pos)
        self.vel = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * random.randint(100,
                                                                                                                  300)
        self.radius = random.randint(10, 25)
        self.color = color
        self.life = 1.0

        # Create a surface with per-pixel alpha for the glow
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=pos)

    def update(self, dt):
        self.life -= dt
        self.pos += self.vel * dt
        self.rect.center = self.pos

        # Shrink
        if self.life > 0:
            scale = int(self.radius * 2 * self.life)
            if scale > 0:
                self.image = pygame.transform.scale(self.image, (scale, scale))
                self.rect = self.image.get_rect(center=self.rect.center)
        else:
            self.kill()


# --- SETUP ---
shaker = ShakeManager()
particles = pygame.sprite.Group()

while True:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Left Click: Big Boom
            if event.button == 1:
                shaker.add_trauma(1.0)  # Max Trauma
                for _ in range(20):
                    particles.add(GlowParticle(event.pos, (255, 100, 50)))  # Orange Fire

            # Right Click: Small Bump
            if event.button == 3:
                shaker.add_trauma(0.3)

    # 1. Update Logic
    shaker.update(dt)
    particles.update(dt)

    # 2. Draw World (To the temporary surface)
    world_surf.fill((30, 30, 40))

    # Draw Grid (to see movement easier)
    for x in range(0, 800, 50):
        pygame.draw.line(world_surf, (50, 50, 60), (x, 0), (x, 600))
    for y in range(0, 600, 50):
        pygame.draw.line(world_surf, (50, 50, 60), (0, y), (800, y))

    # Draw Particles with ADDITIVE blending (The Glow Trick)
    # We have to draw them manually to use the blend flag
    for p in particles:
        # BLEND_ADD makes colors stack and get brighter
        world_surf.blit(p.image, p.rect, special_flags=pygame.BLEND_ADD)

    # 3. Final Render (Apply Shake)
    offset = shaker.get_offset()
    display_surface.fill((0, 0, 0))  # Clean edges
    display_surface.blit(world_surf, offset)

    pygame.display.update()