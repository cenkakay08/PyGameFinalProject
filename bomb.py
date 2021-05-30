import pygame
import random
from settings import *
vec = pygame.math.Vector2


class Bomb(pygame.sprite.Sprite):
    def __init__(self, player):
        self.player = player
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILE_W, TILE_H*1.7))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, WIDTH-50)
        self.rect.y = -50
        self.isDropping = True
        self.explodeDelay = 150

    def update(self):

        if self.isDropping:
            self.rect.y += 2
        else:
            if self.explodeDelay <=0:
                self.kill()
            else:
                self.explodeDelay -= 1

        if self.rect.bottom >= TILE_W*28:
            self.image = pygame.Surface((TILE_W*1.7, TILE_H))
            self.image.fill(PURPLE)
            self.isDropping = False
            self.rect.bottom = TILE_W*29
        
        hits = pygame.sprite.collide_rect(self.player, self)
        if hits:
            self.player.isDead = True