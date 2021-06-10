import pygame
from settings import *


class Guided_Missile(pygame.sprite.Sprite):
    def __init__(self, player, x, y):
        self.player = player
        #Load Frames
        self.skull_frame = pygame.image.load("resources/image/enemy/skull.png").convert_alpha()
        self.skull_frame_r = pygame.image.load("resources/image/enemy/skull_r.png").convert_alpha()
        self.skull_frame_l = pygame.image.load("resources/image/enemy/skull_l.png").convert_alpha()
        #Load sound effect
        self.shot_sound = pygame.mixer.Sound('resources/sound/shot.wav')
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

                self.shot_sound.play()
            elif self.player.rect.left < self.rect.x < self.player.rect.right:
                self.inYRange = True
                if self.player.rect.y < self.rect.y:
                    self.towards = -1

                self.shot_sound.play()

        if self.inXRange:
            self.rect.x += self.towards*3
        elif self.inYRange:
            self.rect.y += self.towards*3
        else:
            self.rect.y += 2

        hits = pygame.sprite.collide_rect_ratio(0.8)(self.player, self)
        if hits:
            self.player.playerDied()

          #remove guided missiles out of screen
        if self.rect.top > HEIGHT or self.rect.left > WIDTH:
            self.kill()

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
        

