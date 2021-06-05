import pygame
import random
import sys
sys.path.insert(1,'../../')
from settings import *
vec = pygame.math.Vector2


class Bomb(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILE_W, TILE_H))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, WIDTH-50)
        self.rect.y = -50
        self.isDropping = True
        self.onFuse = True
        self.last_update = None
        self.explodeDelay = 300
        self.fuseDelay = 500

    def update(self):
        #if hits a platform stops
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)

        if hits and self.isDropping:
            self.isDropping = False
            self.rect.bottom = hits[0].rect.top
            self.last_update = pygame.time.get_ticks()
        
        if self.isDropping:
            self.rect.y += 2
        else:
            self.explode()
        
        hits = pygame.sprite.collide_rect(self.game.player, self)
        if hits:
            self.game.player.isDead = True

    def explode(self):
        now = pygame.time.get_ticks()

        if self.onFuse:
            if now - self.last_update > self.fuseDelay:
                self.onFuse = False
                self.last_update = now

        else:
            self.image = pygame.Surface((TILE_W*1.5, TILE_H*1.5))
            self.image.fill(PURPLE)
            self.rect = self.image.get_rect(bottom=(self.rect.bottom),centerx=(self.rect.centerx))

            if now-self.last_update > self.explodeDelay:
                self.kill()