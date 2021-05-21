import pygame
from settings import *
vec = pygame.math.Vector2


class Ladder(pygame.sprite.Sprite):
    def __init__(self, x , y, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, h))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y