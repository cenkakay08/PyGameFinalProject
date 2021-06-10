import pygame
from settings import *


class One_Up(pygame.sprite.Sprite):
    def __init__(self, x , y, game):
        pygame.sprite.Sprite.__init__(self)
        self.oneUp_frame = pygame.image.load("resources/image/misc/hearth.png").convert_alpha()
        self.sound = pygame.mixer.Sound('resources/sound/oneUP.wav')
        self.game = game
        self.image = self.oneUp_frame
        self.image = pygame.transform.scale(self.image,(TILE_W,TILE_H))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):

        hits = pygame.sprite.collide_rect(self.game.player, self)
        if hits:
            self.game.health += 1
            self.sound.play()
            self.kill()