import pygame
import random
from settings import *
vec = pygame.math.Vector2


class Missile(pygame.sprite.Sprite):
    def __init__(self, player):
        self.player = player
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, WIDTH-50)
        self.rect.y = -50

    def update(self):

        self.rect.y += 3

        hits = pygame.sprite.collide_rect(self.player, self)
        if hits:
            self.player.isDead = True