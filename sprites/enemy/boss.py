import pygame
import sys
from settings import *
import random


class Boss(pygame.sprite.Sprite):
    def __init__(self, player):
        self.player = player
        self.boss_frames = [pygame.image.load("resources/image/enemy/boss_1.png").convert_alpha(),pygame.image.load("resources/image/enemy/boss_2.png").convert_alpha()]
        pygame.sprite.Sprite.__init__(self)
        self.boss_sound = pygame.mixer.Sound('resources/sound/boss.wav')
        self.image = self.boss_frames[0]
        self.image = pygame.transform.scale(self.image,(TILE_H*6,TILE_H*6))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.y = -50
        self.isDropping = True
        self.current_frame = 0
        self.last_update = 0
        self.isLeft = False
        self.waitOnCenter = 200
        self.current_waitOnCenter = self.waitOnCenter
        self.soundPayed = False

    def update(self):
        
        if self.isDropping:
            self.drop()
            self.current_waitOnCenter = self.waitOnCenter
            self.soundPayed = False
        else:

            if self.current_waitOnCenter <= 0:
                if not self.soundPayed:
                    self.boss_sound.play()
                    self.soundPayed = True
                self.turn()
            else:
                self.current_waitOnCenter -= 1

        #check player is dead
        hits = pygame.sprite.collide_mask(self, self.player)
        if hits:
            self.player.playerDied()

        
        self.animate()

    def drop(self):
        self.rect.y +=3

        if self.rect.centery > HEIGHT/2:
            self.rect.centery = HEIGHT/2
            self.isDropping = False
            self.isLeft = bool(random.getrandbits(1))

    def turn(self):
        if self.isLeft:
            self.rect.x -= 10
        else:
            self.rect.x += 10

        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.rect.midbottom = (WIDTH/2, -50)
            self.isDropping = True


    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 400:
            self.current_frame = (self.current_frame + 1) %len(self.boss_frames)
            bottom = self.rect.bottom
            left = self.rect.left
            self.image = self.boss_frames[self.current_frame]
            self.image = pygame.transform.scale(self.image,(TILE_H*6,TILE_H*6))
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
            self.rect.left = left
            self.last_update = now
        self.mask = pygame.mask.from_surface(self.image)
