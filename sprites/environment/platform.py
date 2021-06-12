import pygame
from settings import *


class Platform(pygame.sprite.Sprite):
    def __init__(self, x , y, left, right):
        pygame.sprite.Sprite.__init__(self)
        
        self.platform_frame = pygame.image.load("resources/image/environment/platform.png").convert_alpha()

        self.image = self.platform_frame
        self.image = pygame.transform.scale(self.image,(TILE_W,TILE_H))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        #platform group used ford robot ai for know when they should turn back
        self.platformGroup = [left, right]
