import pygame
import random
import sys
sys.path.insert(1,'../../')
from settings import *
vec = pygame.math.Vector2


class Missile(pygame.sprite.Sprite):
    def __init__(self, player):
        self.player = player
        self.vase_frame = pygame.image.load("resources/image/enemy/vase.png").convert_alpha()
        pygame.sprite.Sprite.__init__(self)
        self.image = self.vase_frame
        self.image = pygame.transform.scale(self.image,(TILE_W,int(TILE_H*1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, WIDTH-50)
        self.rect.y = -50

    def update(self):

        self.rect.y += 3

        hits = pygame.sprite.collide_rect_ratio(0.8)(self.player, self)
        if hits:
            self.player.playerDied()
            
        #remove missiles out of screen
        if self.rect.top > HEIGHT:
            self.kill()