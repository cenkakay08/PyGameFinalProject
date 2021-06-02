import pygame
import sys
sys.path.insert(1,'../../')
from settings import *
vec = pygame.math.Vector2
import random


class Robot(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.stand_frames_r = pygame.image.load("resources/image/enemy/robot/stand.png").convert_alpha()
        self.stand_frames_l = pygame.transform.flip(self.stand_frames_r,True,False)
        self.climb_frames_r = [pygame.image.load("resources/image/enemy/robot/stand.png").convert_alpha(),pygame.image.load("resources/image/enemy/robot/climb.png").convert_alpha()]
        self.climb_frames_l =[]
        for frame in self.climb_frames_r:
            self.climb_frames_l.append(pygame.transform.flip(frame,True,False))
        self.run_frames_r = [pygame.image.load("resources/image/enemy/robot/run_1.png").convert_alpha(),pygame.image.load("resources/image/enemy/robot/run_2.png").convert_alpha(),pygame.image.load("resources/image/enemy/robot/run_3.png").convert_alpha(),pygame.image.load("resources/image/enemy/robot/run_4.png").convert_alpha(),pygame.image.load("resources/image/enemy/robot/run_5.png").convert_alpha()]
        self.run_frames_l = []
        for frame in self.run_frames_r:
            self.run_frames_l.append(pygame.transform.flip(frame,True,False))
        self.game = game
        pygame.sprite.Sprite.__init__(self)
        self.image = self.stand_frames_r
        self.image = pygame.transform.scale(self.image,(30,40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.isClimbing = False
        self.climbedLadder = None
        self.standingPlatform = None
        self.goRight = True 
        self.climbUp = True
        self.current_frame = 0
        self.last_update = 0
        self.runClimbAnimation = False
        self.isLeft = False

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
                if self.rect.centery > (self.climbedLadder.ladderGroup[0]-self.climbedLadder.ladderGroup[1])/2:
                    self.climbUp = True
                else:
                    self.climbUp =False

        else:
            self.climb()

        #check player is dead
        hits = pygame.sprite.collide_rect(self.game.player, self)
        if hits:
            self.game.player.playerDied()

        
        self.animate()

    def walk(self):
        if self.standingPlatform != None:
                if self.goRight:

                    if self.rect.right < self.standingPlatform.platformGroup[1]-3:
                        self.rect.x +=2
                        self.isLeft = False
                    else:
                        self.goRight = False
                else:
                    if self.rect.left > self.standingPlatform.platformGroup[0]+3:
                        self.rect.x -=2
                        self.isLeft = True
                    else:
                        self.goRight = True

    def climb(self):

        if self.climbedLadder != None:
                if self.climbUp:

                    if self.rect.centery > self.climbedLadder.ladderGroup[1]:
                        self.rect.y -=3
                    else:
                        self.isClimbing = False
                else:
                    if self.rect.bottom < self.climbedLadder.ladderGroup[0]:
                        self.rect.y +=3
                    else:
                        self.isClimbing = False

    def animate(self):
        now = pygame.time.get_ticks()
        if self.isClimbing:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) %len(self.climb_frames_r)
                bottom = self.rect.bottom
                left = self.rect.left
                if self.isLeft:
                    self.image = self.climb_frames_l[self.current_frame]
                else:
                    self.image = self.climb_frames_r[self.current_frame]
                self.image = pygame.transform.scale(self.image,(30,40))
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                self.rect.left = left
        else:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) %len(self.run_frames_r)
                bottom = self.rect.bottom
                left = self.rect.left
                if self.isLeft:
                    self.image = self.run_frames_l[self.current_frame]
                else:
                    self.image = self.run_frames_r[self.current_frame]
                self.image = pygame.transform.scale(self.image,(30,40))
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                self.rect.left = left
