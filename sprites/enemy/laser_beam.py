import pygame
import random
import sys
sys.path.insert(1,'../../')
from settings import *


class LaserBeam(pygame.sprite.Sprite):
    def __init__(self, player):
        self.player = player
        pygame.sprite.Sprite.__init__(self)
        self.beam_frame = pygame.image.load("resources/image/enemy/beam.png").convert_alpha()
        self.image = pygame.Surface((WIDTH/4, TILE_H*0.5))
        self.image.fill(BEAM)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.centery = self.player.rect.centery
        self.chargingTime = 100
        self.firstTime = True

    def update(self):
        if self.chargingTime <=0:
            
            if self.firstTime:
                self.image = self.beam_frame
                self.image = pygame.transform.scale(self.image,(int(WIDTH/2),TILE_H*4))
                self.rect = self.image.get_rect(midright=(-50,self.rect.y))

            self.firstTime = False
            
            self.rect.x += 8
            
            if self.rect.left > WIDTH:
                self.kill()

            hits = pygame.sprite.collide_rect(self.player, self)
            if hits:
                self.player.playerDied()


        else:
            self.rect.centery = self.player.rect.centery
            self.chargingTime -= 1