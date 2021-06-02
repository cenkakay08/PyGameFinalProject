import pygame
import sys
sys.path.insert(1,'../../')
from settings import *
vec = pygame.math.Vector2


class Guided_Missile(pygame.sprite.Sprite):
    def __init__(self, player, x, y):
        self.player = player
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill(DARKRED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.inXRange = False
        self.inYRange  =False
        self.towards = 1

    def update(self):
        
        if not self.inXRange and not self.inYRange:
            if self.player.rect.top < self.rect.y < self.player.rect.bottom:
                self.inXRange = True
                if self.player.rect.x < self.rect.x:
                    self.towards = -1
            elif self.player.rect.left < self.rect.x < self.player.rect.right:
                self.inYRange = True
                if self.player.rect.y < self.rect.y:
                    self.towards = -1

        if self.inXRange:
            self.rect.x += DIF*self.towards
        elif self.inYRange:
            self.rect.y += (DIF+2)*self.towards
        else:
            self.rect.y += 2

        hits = pygame.sprite.collide_rect(self.player, self)
        if hits:
            self.player.playerDied()