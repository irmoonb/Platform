import math
import random
import tty
import pygame
import sys

class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super(Character, self).__init__()
        self.image = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
        self.image.convert_alpha()
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))

    def move(self, deltax, deltay):
        if self.rect.left < 0 or self.rect.right > 1200:
            deltax *= -3
        if self.rect.top < 0 or self.rect.bottom > 600:
            deltay *= -3

        self.rect.centerx += deltax
        self.rect.centery += deltay


# Initialize Pygame and give access to all the methods in the package
pygame.init()

# Set up the screen dimensions
screen_width = 1200
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Agario")

# Create clock to later control frame rate
clock = pygame.time.Clock()

sq1 = Character(100, 300, "red")
characters = pygame.sprite.Group()
characters.add(sq1)

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():  # pygame.event.get()
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))

    # Get the state of all keys
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        sq1.move(-2, 0)
    if keys[pygame.K_d]:
        sq1.move(2, 0)
    if keys[pygame.K_w]:
        sq1.move(0, -2)
    if keys[pygame.K_s]:
        sq1.move(0, 2)

    characters.draw(screen)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()