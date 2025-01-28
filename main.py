import pygame
import sys
import random
import math


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        """
        This function is to initialize the character with all of its attributes.
        This inludes the appearance, and a variable initialized for checking if
        it's on the floor. If not, apply gravity.

        :param x:
        :param y:
        :param color:
        """
        super(Character, self).__init__()
        self.image = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
        self.image.convert_alpha()
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.on_ground = False

    def move(self, deltax, deltay):
        """
        This function enables the character to be moved.

        :param deltax:
        :param deltay:
        :return:
        """
        self.rect.x += deltax
        self.rect.y += deltay

    def gravity(self):
        """
        This function enables for gravity to be applied to the character,
        IF they are not on a surface.

        :return:
        """
        if not self.on_ground:
            self.velocity_y += 1
            self.rect.y += self.velocity_y

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super(Platform, self).__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))

# Initialize Pygame and give access to all the methods in the package
pygame.init()

# Set up the screen dimensions
screen_width = 1200
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Agario")

# Create clock to later control frame rate
clock = pygame.time.Clock()

# Add 2 characters
characters = pygame.sprite.Group()
sq1 = Character(1100, 300, "red")
sq2 = Character(100, 300, "pink")
characters.add(sq1)
characters.add(sq2)

# Add 3 platforms
platforms = pygame.sprite.Group()
platform1 = Platform(300, 400, 200, 20, "white")
platform2 = Platform(700, 300, 200, 20, "red")
platform3 = Platform(500, 500, 200, 20, "pink")
platforms.add(platform1, platform2, platform3)

# Main game loop
running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                sq1.jump()
            if event.key -- pygame.K_w:
                sq2.jump()

    # Get the state of all keys
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        sq1.move(-5, 0)
    if keys[pygame.K_RIGHT]:
        sq1.move(5, 0)
    if keys[pygame.K_a]:
        sq2.move(-5, 0)
    if keys[pygame.K_d]:
        sq2.move(5, 0)

    for character in characters:
        character.gravity()
        character.on_ground = False # Apply gravity ALWAYS, just like the real world

        for platform in platforms:
            if character.rect.colliderect(platform.rect) and character.velocity_y > 0:
                character.on_ground = True
                character.velocity_y = 0
                character.rect.bottom = platform.rect.top

    platforms.draw(screen)
    characters.draw(screen)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()