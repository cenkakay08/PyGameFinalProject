import pygame
import sys
sys.path.insert(1,'../enemy/')
from settings import *
vec = pygame.math.Vector2


class Coin(pygame.sprite.Sprite):
    def __init__(self, x , y, player):
        self.player = player
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.isPicked = False

    def update(self):

        #This way coin class did not need to know about whole game class
        hits = pygame.sprite.collide_rect(self.player, self)
        if hits:
            self.isPicked = True