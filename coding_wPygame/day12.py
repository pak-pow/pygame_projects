import pygame
import sys
import random

from pygame.locals import *  # Imports useful constants like QUIT

# Creating a class for the particles that inherits from Pygame's Sprite class
class Particle(pygame.sprite.Sprite):

    def __init__(self, pos, color):
        # Initialize the parent Sprite class so Pygame recognizes this object
        super().__init__()

        # Randomly choose a starting size between 4 and 10 pixels
        self.SIZE = random.randint(4, 10)

        # Store the color we eventually want it to be (Red or Blue)
        self.target_color = color

        # Set the starting color to White (255, 255, 255)
        self.current_color = (255, 255, 255)

        # Create the visual square surface for the particle
        self.image = pygame.Surface((self.SIZE, self.SIZE))

        # Fill that square with the current color (White at first)
        self.image.fill(self.current_color)

        # Get the rectangle area of the image and center it at the mouse position
        self.rect = self.image.get_rect(center=pos)

        # Store position as a Vector2 for precise math (floating point numbers)
        self.pos = pygame.math.Vector2(pos)

        # Pick a random X and Y direction between -1 (left/up) and 1 (right/down)
        self.velocity = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))

        # Safety check: If random picked (0,0), force it to move up so it doesn't freeze
        if self.velocity.length() == 0:
            self.velocity = pygame.math.Vector2(0, -1)

        # Normalize keeps the direction but resets length to 1, then we multiply by speed (50-200)
        self.velocity = self.velocity.normalize() * random.randint(50, 200)

        # Set how many seconds this particle lives (between 0.2 and 0.6 seconds)
        self.lifetime = random.uniform(0.2, 0.6)

        # Save the starting lifetime so we can calculate the percentage later
        self.start_lifetime = self.lifetime

    def update(self, dt):
        # Move the position based on velocity and time passed (dt)
        self.pos += self.velocity * dt

        # Update the rectangle position (must be integers for pixels)
        self.rect.center = (int(self.pos.x), int(self.pos.y))

        # Decrease the lifetime counter
        self.lifetime -= dt

        # If lifetime runs out...
        if self.lifetime <= 0:
            self.kill()  # ...delete the particle from all groups

        # --- COLOR FADE LOGIC ---

        # Calculate percentage of life left (0.0 to 1.0)
        life_ratio = self.lifetime / self.start_lifetime

        # Ensure the ratio stays strictly between 0 and 1 (prevents color glitches)
        life_ratio = max(0, min(1, life_ratio))

        # Math to mix the colors: Start White, fade to Target Color based on ratio
        # Formula: Target + (Difference) * Percentage
        r = int(self.target_color[0] + (255 - self.target_color[0]) * life_ratio)
        g = int(self.target_color[1] + (255 - self.target_color[1]) * life_ratio)
        b = int(self.target_color[2] + (255 - self.target_color[2]) * life_ratio)

        # Update the particle's current color variable
        self.current_color = (r, g, b)

        # --- SHRINKING LOGIC ---

        if self.SIZE > 0:
            # Shrink the size by 10 pixels per second
            self.SIZE -= 10 * dt

            # If it gets too small, set it to 0
            if self.SIZE < 1:
                self.SIZE = 0

            # Re-draw the surface with the new smaller size
            # SRCALPHA allows for transparency if we wanted it
            self.image = pygame.Surface((int(self.SIZE), int(self.SIZE)), pygame.SRCALPHA)

            # Fill the new smaller square with the calculated faded color
            self.image.fill(self.current_color)


class Main:
    def __init__(self):
        # Initialize all Pygame modules
        pygame.init()

        # Screen settings
        self.DISPLAY_WIDTH = 800
        self.DISPLAY_HEIGHT = 600

        # Create the window
        self.DISPLAY = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))

        # Create a clock to control the frame rate
        self.CLOCK = pygame.time.Clock()
        self.FPS = 60

    def run(self):
        # Create a group to hold and manage all particles
        particle_group = pygame.sprite.Group()

        # Infinite loop to keep the game running
        while True:
            # Calculate delta time (dt) - converts milliseconds to seconds
            # This ensures movement is smooth regardless of computer speed
            dt = self.CLOCK.tick(self.FPS) / 1000

            # Event Loop: Listen for inputs
            for event in pygame.event.get():

                # If X button is clicked, close the app
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                # LEFT CLICK: Create an explosion of Red particles
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i in range(30):  # Create 30 particles at once
                        p = Particle(event.pos, (250, 50, 50))  # Red color
                        particle_group.add(p)  # Add to group

            # Check if mouse buttons are being held down
            mouse_buttons = pygame.mouse.get_pressed()

            # RIGHT CLICK (index 2): Create a stream of Blue particles
            if mouse_buttons[2]:
                pos = pygame.mouse.get_pos()
                for i in range(2):  # Create 2 particles per frame (stream effect)
                    p = Particle(pos, (50, 200, 255))  # Blue color
                    particle_group.add(p)

            # Update every single particle in the group (moves and shrinks them)
            particle_group.update(dt)

            # Clear the screen with a dark gray background
            self.DISPLAY.fill((50, 50, 50))

            # Draw all particles onto the screen
            particle_group.draw(self.DISPLAY)

            # Flip the display to show the new frame
            pygame.display.update()


# Standard boilerplate to run the Main class only if this file is run directly
if __name__ == "__main__":
    app = Main()
    app.run()