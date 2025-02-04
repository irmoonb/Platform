import pygame
import sys
import random
import math

from setuptools.msvc import PlatformInfo

# Initialize Pygame and give access to all the methods in the package
pygame.init()

# Set up the screen dimensions
screen_width = 1200
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Agario")

# Create clock to later control frame rate
clock = pygame.time.Clock()

# Initialize colors
GRAY = (200, 200, 200)
RED = (255, 0, 0)
PINK = (255, 105, 180)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

#######################################################
# CLASS: Character
#######################################################

class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, color, live_color):
        """
        This function is to initialize the character with all of its attributes.
        This inludes the appearance, and a variable initialized for checking if
        it's on the floor. If not, apply gravity.

        :param x:
        :param y:
        :param color:
        """
        super(Character, self).__init__()
        self.image = pygame.Surface((50, 50))
        self.image.convert_alpha()
        self.image.fill(color)
        self.rect = self.image.get_rect(midbottom = (x, y))
        self.velocity_y = 0
        self.on_ground = False
        self.live_color = live_color
        self.alive = True

    def move(self, deltax, deltay):
        """
        This function enables the character to be moved.

        :param deltax:
        :param deltay:
        :return:
        """
        if self.alive:
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
        else:
            self.velocity_y = 0
        self.rect.y += self.velocity_y

    def jump(self):
        if self.on_ground and self.alive:
            self.velocity_y -= 15
            self.on_ground = False # GRAVITY IS ALWAYS HERE

    def death(self, platforms):
        if self.rect.top > screen_height: # AKA, if a player falls off
            self.alive = False # They die!
            print("A player died!")
            return

        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if platform.color != self.live_color and platform.color != GRAY:
                    self.alive = False
                    print("A player landed on the wrong platform and died!")
                    return

        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if platform.color != self.live_color and platform.color != (200, 200, 200):
                    self.alive = False
                    print("A player died!")
                    return

#######################################################
# CLASS: Platform
#######################################################

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, speed_x = 0, speed_y = 0, move_range = 0):
        super(Platform, self).__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.color = color
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.start_x = x
        self.start_y = y
        self.move_range = move_range
        self.direction = 1

    def move(self):
        if self.move_range > 0:
            self.rect.x += self.speed_x * self.direction
            self.rect.y += self.speed_y * self.direction

            if abs(self.rect.x - self.start_x) >= self.move_range or abs(self.rect.y - self.start_y) >= self.move_range:
                self.direction *= -1

#######################################################
# CLASS: ENEMY
#######################################################
class Enemy(pygame.sprite.Sprite):
    def __init__(self, platform, speed = 2):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(midbottom=(platform.rect.x + platform.rect.width / 2, platform.rect.top))
        self.platform = platform
        self.speed = speed
        self.direction = 1
        self.on_ground = True

    def move(self):
        # self.rect.x += self.speed * self.direction
        #
        # if self.rect.left <= self.platform.rect.left or self.rect.right >= self.platform.rect.right:
        #     self.direction *= -1
        #
        # self.rect.bottom = self.platform.rect.top
        if self.on_ground:
            self.rect.x += self.speed * self.direction

            if self.rect.left <= self.platform.rect.left or self.rect.right >= self.platform.rect.right:
                self.direction *= -1

            if self.rect.right < self.platform.rect.left or self.rect.left > self.platform.rect.right:
                self.on_ground = False
        else:
            self.gravity_enemy()

    def gravity_enemy(self, platforms):
        if not self.on_ground:
            self.velocity_y += 1
        else:
            self.velocity_y = 0

        self.rect.y += self.velocity_y

        self.one_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.velocity_y >= 0:
                self.on_ground = True
                self.velocity_y = 0
                self.rect.bottom = platform.rect.top

        if self.rect.top > screen_height:
            print("Enemy is eliminated.")
            self.kill()

def check_collision(characters, enemy):
    for character in characters:
        if character.alive and character.rect.colliderect(enemy.rect):
            character.alive = False
            print("A player made contact with enemy and died!")

# Add 2 characters
characters = pygame.sprite.Group()
sq1 = Character(1100, 450, RED, RED)
sq2 = Character(100, 450, PINK, PINK)
characters.add(sq1)
characters.add(sq2)

# Add 4 platforms
platforms = pygame.sprite.Group()
platform1 = Platform(50, 500, 200, 20, GRAY)
platform2 = Platform(1000, 500, 200, 20, RED)
platform3 = Platform(325, 500, 600, 20, PINK)
platform4 = Platform(500, 350, 200, 20, GRAY, speed_x=2, move_range=400)
platforms.add(platform1, platform2, platform3, platform4)

# Add enemy
enemy = Enemy(platform4)
enemies = pygame.sprite.Group()
enemies.add(enemy)

for character in characters:
    for platform in platforms:
        if character.rect.colliderect(platform.rect):
            if platform.color == character.live_color or platform.color == GRAY:
                character.on_ground = True

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
            if event.key == pygame.K_w:
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

    for platform in platforms:
        platform.move()

    for character in characters:
        character.on_ground = False

        for platform in platforms:
            if character.rect.colliderect(platform.rect) and character.velocity_y >= 0:
                character.on_ground = True
                character.velocity_y = 0
                character.rect.bottom = platform.rect.top

        character.gravity()
        character.death(platforms)

    enemy.move()
    enemy.gravity_enemy(platforms)

    check_collision(characters, enemy)

    platforms.draw(screen)
    for character in characters:
        if character.alive:
            screen.blit(character.image, character.rect.topleft)
    characters.draw(screen)
    enemies.draw(screen)

    if not sq1.alive or not sq2.alive:
        print("Game over. Exiting... 3 seconds...")
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()