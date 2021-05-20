import pygame
from settings import *
vec = pygame.math.Vector2


class Platform(pygame.sprite.Sprite):
    def __init__(self, x , y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
