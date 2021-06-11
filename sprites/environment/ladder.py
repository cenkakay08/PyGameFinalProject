import pygame
from settings import *


class Ladder(pygame.sprite.Sprite):
    def __init__(self, x , y, top, bottom):
        self.ladder_frame = pygame.image.load("resources/image/environment/ladder.png").convert_alpha()
        pygame.sprite.Sprite.__init__(self)
        self.image = self.ladder_frame
        self.image = pygame.transform.scale(self.image,(TILE_W,TILE_H))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        #ladder group used for ladder end points
        self.ladderGroup = [bottom,top]