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
        self.inRange = False

    def update(self):

        if self.rect.y > self.player.rect.top and self.rect.y < self.player.rect.bottom:
            self.inRange = True

        if self.inRange:
            self.rect.x += 3
        else:
            self.rect.y += 2

        hits = pygame.sprite.collide_rect(self.player, self)
        if hits:
            print("hit")