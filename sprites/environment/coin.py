import pygame
import sys
sys.path.insert(1,'sprites/enemy/')
from settings import *
vec = pygame.math.Vector2


class Coin(pygame.sprite.Sprite):
    def __init__(self, x , y, player):
        self.coin_frames = [pygame.image.load("resources/image/coin/coin_1.png").convert_alpha(),pygame.image.load("resources/image/coin/coin_2.png").convert_alpha(),pygame.image.load("resources/image/coin/coin_3.png").convert_alpha(),pygame.image.load("resources/image/coin/coin_4.png").convert_alpha(),pygame.image.load("resources/image/coin/coin_5.png").convert_alpha()]
        self.player = player
        pygame.sprite.Sprite.__init__(self)
        self.image = self.coin_frames[0]
        self.image = pygame.transform.scale(self.image,(TILE_W,TILE_H))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.isPicked = False
        self.current_frame = 0
        self.last_update = 0

    def update(self):
        self.animate()

        #This way coin class did not need to know about whole game class
        hits = pygame.sprite.collide_rect(self.player, self)
        if hits:
            effect = pygame.mixer.Sound('resources/sound/coin.wav')
            effect.play()
            self.isPicked = True

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 200:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) %len(self.coin_frames)
            bottom = self.rect.bottom
            left = self.rect.left
            self.image = self.coin_frames[self.current_frame]
            self.image = pygame.transform.scale(self.image,(TILE_W,TILE_H))
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
            self.rect.left = left