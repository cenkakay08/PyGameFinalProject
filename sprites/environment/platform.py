import pygame
import sys
sys.path.insert(1,'../enemy/')
from settings import *
vec = pygame.math.Vector2


class Platform(pygame.sprite.Sprite):
    def __init__(self, x , y):
        self.platform_frame = pygame.image.load("resources/image/environment/platform.png").convert()
        pygame.sprite.Sprite.__init__(self)
        self.image = self.platform_frame
        self.image = pygame.transform.scale(self.image,(TILE_W,TILE_H))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
