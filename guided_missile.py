import pygame
from settings import *
vec = pygame.math.Vector2


class Guided_Missile(pygame.sprite.Sprite):
    def __init__(self, player):
        self.player = player
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill(DARKRED)
        self.rect = self.image.get_rect()
        self.rect.x = 30
        self.rect.y = -50
        self.inXRange = False
        self.inYRange  =False

    def update(self):
        
        if not self.inXRange and not self.inYRange:
            if self.player.rect.top < self.rect.y < self.player.rect.bottom:
                self.inXRange = True
            elif self.player.rect.left < self.rect.x < self.player.rect.right:
                self.inYRange = True

        if self.inXRange:
            self.rect.x += DIF
        elif self.inYRange:
            self.rect.y += DIF
        else:
            self.rect.y += 2

        hits = pygame.sprite.collide_rect(self.player, self)
        if hits:
            self.player.isDead = True