import pygame
from settings import *


class Platform(pygame.sprite.Sprite):
    def __init__(self, x , y, left, right):
        self.platform_frame = pygame.image.load("resources/image/environment/platform.png").convert_alpha()
        pygame.sprite.Sprite.__init__(self)
        self.image = self.platform_frame
        self.image = pygame.transform.scale(self.image,(TILE_W,TILE_H))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.platformGroup = [left, right]
