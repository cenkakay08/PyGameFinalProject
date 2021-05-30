import pygame
from settings import *
vec = pygame.math.Vector2
import random


class Robot(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.isClimbing = False
        self.climbedLadder = None
        self.standingPlatform = None
        self.goRight = True 
        self.climbUp = True

    def update(self):
        
        if not self.isClimbing:
            self.rect.y += 5
            hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
    
            if hits:
                self.rect.bottom = hits[0].rect.top+1
                self.standingPlatform = hits[0]

            
            self.walk()

            hits = pygame.sprite.spritecollide(self, self.game.ladders, False)
            if hits and random.randint(0,100) < 1:
                self.isClimbing = True
                self.climbedLadder = hits[0]
                self.rect.centerx = self.climbedLadder.rect.centerx
                if self.rect.centery > self.climbedLadder.rect.centery:
                    self.climbUp = True
                else:
                    self.climbUp =False

        else:
            self.climb()

        #check player is dead
        hits = pygame.sprite.collide_rect(self.game.player, self)
        if hits:
            self.game.player.isDead = True

    def walk(self):
        if self.standingPlatform != None:
                if self.goRight:

                    if self.rect.right < self.standingPlatform.rect.right-3:
                        self.rect.x +=3
                    else:
                        self.goRight = False
                else:
                    if self.rect.left > self.standingPlatform.rect.left+3:
                        self.rect.x -=3
                    else:
                        self.goRight = True

    def climb(self):

        if self.climbedLadder != None:
                if self.climbUp:

                    if self.rect.centery > self.climbedLadder.rect.top:
                        self.rect.y -=3
                    else:
                        self.isClimbing = False
                else:
                    if self.rect.bottom < self.climbedLadder.rect.bottom:
                        self.rect.y +=3
                    else:
                        self.isClimbing = False
