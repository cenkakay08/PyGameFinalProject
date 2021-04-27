# Pygame sprite Example
import os
import random
import math
import pygame

WIDTH = 800
HEIGHT = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")


class Player(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self):
        # this line is required to properly create the sprite
        pygame.sprite.Sprite.__init__(self)
        # create a plain rectangle for the sprite image
        # convert() makes optimazation on image and being faster.
        self.image = pygame.image.load(
            os.path.join(img_folder, "p1_jump.png")).convert()
        self.image.set_colorkey(BLACK)

        # find the rectangle that encloses the image
        self.rect = self.image.get_rect()
        # center the sprite on the screen
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.x_speed = 0
        self.y_speed = 0

    def update(self, X):
        # any code here will happen every time the game loop updates
        self.x_speed = 0
        self.y_speed = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.x_speed = -5
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.x_speed = 5
        if keystate[pygame.K_UP] or keystate[pygame.K_w]:
            self.y_speed = -5
        if keystate[pygame.K_DOWN] or keystate[pygame.K_s]:
            self.y_speed = 5
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed


class Enemies(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # create a plain rectangle for the sprite image
        # convert() makes optimazation on image and being faster.
        self.image = pygame.image.load(
            os.path.join(img_folder, "p1_hurt.png")).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.speed = 2

        # find the rectangle that encloses the image

        self.rect.center = self.get_random_coordinate_for_enemy_spawn()

    def update(self, player):
        self.catch_player(player)

    def catch_player(self, player):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx, dy = dx / dist, dy / dist
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed
            # Normalize.
        # Move along this normalized vector towards the player at current speed.

        """ if player.rect.x > self.rect.x:
            self.rect.x += self.speed
        if player.rect.y > self.rect.y:
            self.rect.y += self.speed
        if player.rect.x < self.rect.x:
            self.rect.x -= self.speed
        if player.rect.y < self.rect.y:
            self.rect.y -= self.speed """

        """ if player.rect.x > self.rect.x and player.rect.y > self.rect.y:
            self.rect.x += self.speed
            self.rect.y += self.speed
        if player.rect.x < self.rect.x and player.rect.y > self.rect.y:
            self.rect.x -= self.speed
            self.rect.y += self.speed
        if player.rect.x > self.rect.x and player.rect.y < self.rect.y:
            self.rect.x += self.speed
            self.rect.y -= self.speed
        if player.rect.x < self.rect.x and player.rect.y < self.rect.y:
            self.rect.x -= self.speed
            self.rect.y -= self.speed
        if player.rect.x == self.rect.x and player.rect.y > self.rect.y:
            self.rect.y += self.speed
        if player.rect.x == self.rect.x and player.rect.y < self.rect.y:
            self.rect.y -= self.speed
        if player.rect.x > self.rect.x and player.rect.y == self.rect.y:
            self.rect.x += self.speed
        if player.rect.x < self.rect.x and player.rect.y == self.rect.y:
            self.rect.x -= self.speed """

    def get_random_coordinate_for_enemy_spawn(self):

        def area_1():
            random_X = random.randrange(
                0 + int(((self.rect.width)/2)), WIDTH - int(((self.rect.width)/2)))
            random_Y = random.randrange(
                0+(self.rect.height/2), int((HEIGHT/100*40)))
            return (random_X, random_Y)

        def area_2():
            random_X = random.randrange(
                0 + int(((self.rect.width)/2)), WIDTH - int(((self.rect.width)/2)))
            random_Y = random.randrange(
                int((HEIGHT/100*60)+(self.rect.height/2)), HEIGHT - int(self.rect.height/2))
            return (random_X, random_Y)
        area_list = [area_1, area_2]
        return random.choice(area_list)()


# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clean_surface = pygame.Surface((WIDTH, HEIGHT))
pygame.display.set_caption("Sprite Example")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player = Player()
enemies_sprites = pygame.sprite.Group()
for i in range(10):
    enemy = Enemies()
    all_sprites.add(enemy)
    enemies_sprites.add(enemy)


all_sprites.add(player)

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
    # PERFORMANS AZALIRSA DENE all_sprites.clear(screen, clean_surface)
    # Update
    all_sprites.update(player)

    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
