import pygame
import random
import sys
sys.path.insert(1,'../../')
from settings import *


class LasserBeam(pygame.sprite.Sprite):
    def __init__(self, player):
        self.player = player
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = -50
        self.rect.centery = random.randint(50, HEIGHT-50)

    def update(self):

        self.rect.y += 3

        hits = pygame.sprite.collide_rect(self.player, self)
        if hits:
            self.player.isDead = True