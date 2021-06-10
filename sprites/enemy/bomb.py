import pygame
import random
from settings import *


class Bomb(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        pygame.sprite.Sprite.__init__(self)
        self.bomb_frame = pygame.image.load("resources/image/enemy/bomb.png").convert_alpha()
        self.explosion_spritesheet = pygame.image.load("resources/image/enemy/explosion.png")

        self.explosion_frames = []
        for i in range(12):
            image = pygame.Surface((96, 96))
            image.blit(self.explosion_spritesheet, (0, 0), (96*i, 0, 96, 96))
            image = pygame.transform.scale(image, (int(TILE_W*3), int(TILE_H*3)))
            image.set_colorkey(BLACK)
            self.explosion_frames.append(image)

        self.explosion_sound = pygame.mixer.Sound('resources/sound/explosion.wav')

        self.image = self.bomb_frame
        self.image = pygame.transform.scale(self.image,(TILE_W*2,TILE_H*2))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, WIDTH-50)
        self.rect.y = -50
        self.isDropping = True
        self.onFuse = True
        self.last_update = None
        self.last_frameTime = 0
        self.explodeDelay = 300
        self.fuseDelay = 500
        self.current_frame = 0
        self.soundPlayed = False

    def update(self):
        #if hits a platform stops
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)

        if hits and self.isDropping and hits[0].platformGroup[0] <self.rect.centerx < hits[0].platformGroup[1]:
            self.isDropping = False
            self.rect.bottom = hits[0].rect.top
            self.last_update = pygame.time.get_ticks()
        
        if self.isDropping:
            self.rect.y += 2
        else:
            self.explode()
        
        hits = pygame.sprite.collide_rect_ratio(0.8)(self.game.player, self)
        if hits:
            self.game.player.playerDied()

    def explode(self):
        now = pygame.time.get_ticks()

        if self.onFuse:
            if now - self.last_update > self.fuseDelay:
                self.onFuse = False
                self.last_update = now

        else:

            if now - self.last_frameTime > self.explodeDelay/12 and self.current_frame < 11:
                self.last_frameTime = now
                self.current_frame +=1
                

            self.image = self.explosion_frames[self.current_frame]
            
            self.rect = self.image.get_rect(bottom=(self.rect.bottom),centerx=(self.rect.centerx))

            if now-self.last_update > self.explodeDelay:
                self.kill()

            if not self.soundPlayed:
                self.explosion_sound.play()
                self.soundPlayed = True
