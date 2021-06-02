import pygame
import sys
sys.path.insert(1,'../../')
from settings import *
vec = pygame.math.Vector2


class Guided_Missile(pygame.sprite.Sprite):
    def __init__(self, player, x, y):
        self.player = player
        self.skull_frame = pygame.image.load("resources/image/enemy/skull.png").convert_alpha()
        self.skull_frame_r = pygame.image.load("resources/image/enemy/skull_r.png").convert_alpha()
        self.skull_frame_l = pygame.image.load("resources/image/enemy/skull_l.png").convert_alpha()
        pygame.sprite.Sprite.__init__(self)
        self.image = self.skull_frame
        self.image = pygame.transform.scale(self.image,(TILE_W,TILE_H))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.inXRange = False
        self.inYRange  =False
        self.towards = 1

    def update(self):
        self.animate()

        if not self.inXRange and not self.inYRange:
            if self.player.rect.top < self.rect.y < self.player.rect.bottom:
                self.inXRange = True
                if self.player.rect.x < self.rect.x:
                    self.towards = -1
            elif self.player.rect.left < self.rect.x < self.player.rect.right:
                self.inYRange = True
                if self.player.rect.y < self.rect.y:
                    self.towards = -1

        if self.inXRange:
            self.rect.x += DIF*self.towards
        elif self.inYRange:
            self.rect.y += (DIF+2)*self.towards
        else:
            self.rect.y += 2

        hits = pygame.sprite.collide_rect(self.player, self)
        if hits:
            self.player.playerDied()

    def animate(self):
        self.image = self.skull_frame

        if self.inXRange:
            if self.towards ==1:
                self.image = self.skull_frame_r
            else:
                self.image = self.skull_frame_l

        bottom = self.rect.bottom
        left = self.rect.left
        self.image = pygame.transform.scale(self.image,(TILE_W,TILE_H))
        self.rect = self.image.get_rect()
        self.rect.bottom = bottom
        self.rect.left = left
        

