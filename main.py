# Irmoon Batbayar
# Prof. Yin
# 7.3.3
# AP Science Principles: Austin High School

import pygame
import sys
import random
import math

# Initialize Pygame and give access to all the methods in the package
pygame.init()

# Set up the screen dimensions
screen_width = 1200
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rectangle platformer")

# Create clock to later control frame rate
clock = pygame.time.Clock()

# Initialize colors
GRAY = (200, 200, 200)
RED = (255, 0, 0)
PINK = (255, 105, 180)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 128, 0)

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
            self.velocity_y -= 18
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
        self.velocity_y = 0

    def move(self, platforms):
        if self.on_ground and self.platform:
            self.rect.x += self.speed * self.direction

            if self.rect.left <= self.platform.rect.left or self.rect.right >= self.platform.rect.right:
                self.direction *= -1

        else:
            self.gravity_enemy(platforms)

    def gravity_enemy(self, platforms):
        if not self.on_ground:
            self.velocity_y += 1
        else:
            self.velocity_y = 0

        self.rect.y += self.velocity_y

        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.velocity_y >= 0:
                self.on_ground = True
                self.velocity_y = 0
                self.rect.bottom = platform.rect.top
                self.platform = platform
                return

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
platform2 = Platform(1000, 500, 200, 20, GRAY)
platform4 = Platform(300, 200, 600, 20, GRAY)
platformpink = Platform(400, 350, 200, 20, PINK, speed_x = 2, move_range = 350)
platformred = Platform(600, 350, 200, 20, RED, speed_x = 2, move_range = 350)
platformdeath = Platform(100, 155, 50, 5, ORANGE, speed_x = 5, move_range = 900)
platformdeath2 = Platform(300, 325, 50, 5, ORANGE, speed_x = 3, move_range = 900)
platformdeath3 = Platform(500, 450, 50, 5, ORANGE, speed_x = 4, move_range = 600)
platformdeath4 = Platform(500, 450, 50, 4, ORANGE, speed_x = 3, move_range = 700)
platforms.add(platform1, platform2, platform4, platformpink, platformred, platformdeath, platformdeath2, platformdeath3)

# Add enemy
enemy = Enemy(platform4)
enemies = pygame.sprite.Group()
enemies.add(enemy)

for character in characters:
    for platform in platforms:
        if character.rect.colliderect(platform.rect):
            if platform.color == character.live_color or platform.color == GRAY:
                character.on_ground = True

pygame.font.init()

# Main game loop
running = True
while running:
    screen.fill((0, 0, 0))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        sq1.move(-7, 0)
    if keys[pygame.K_RIGHT]:
        sq1.move(7, 0)
    if keys[pygame.K_a]:
        sq2.move(-7, 0)
    if keys[pygame.K_d]:
        sq2.move(7, 0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and sq1.on_ground:
                sq1.jump()
            if event.key == pygame.K_w and sq2.on_ground:
                sq2.jump()

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

    enemy.move(platforms)
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

    # Death/Victory announcements
    if not sq1.alive and sq2.alive:
        font = pygame.font.SysFont("comicsans", 50, bold=True)
        victory_text = font.render("PINK WINS!", True, (255, 105, 180))
        victory_rect = victory_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(victory_text, victory_rect)
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    elif not sq2.alive and sq1.alive:
        font = pygame.font.SysFont("comicsans", 50, bold=True)
        victory_text = font.render("RED WINS!", True, (255, 0, 0))
        victory_rect = victory_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(victory_text, victory_rect)
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

        running = False

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()