import pygame
import random
import sys
sys.path.insert(1,'../../')
from settings import *


class LaserBeam(pygame.sprite.Sprite):
    def __init__(self, player):
        self.player = player
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((WIDTH, TILE_H*0.5))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = -50
        self.rect.centery = random.randint(50, HEIGHT-50)
        self.chargingTime = 200
        self.standingTime = 50

    def update(self):

        if self.chargingTime <=0:
            self.image = pygame.Surface((WIDTH, TILE_H*1.5))
            self.image.fill(WHITE)
            hits = pygame.sprite.collide_rect(self.player, self)
            if hits:
                self.player.isDead = True

            if self.standingTime <= 0:
                self.kill()
            else:
                self.standingTime -= 1

        else:
            self.chargingTime -= 1