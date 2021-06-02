import pygame
import sys
import os
from settings import *
vec = pygame.math.Vector2




class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        self.stand_frames_r = pygame.image.load("resources/image/player/stand.png").convert()
        self.stand_frames_l = pygame.transform.flip(self.stand_frames_r,True,False)
        self.run_frames_r = [pygame.image.load("resources/image/player/run_1.png").convert(),pygame.image.load("resources/image/player/run_2.png").convert(),pygame.image.load("resources/image/player/run_3.png").convert(),pygame.image.load("resources/image/player/run_4.png").convert(),pygame.image.load("resources/image/player/run_5.png").convert()]
        self.run_frames_l = []
        for frame in self.run_frames_r:
            self.run_frames_l.append(pygame.transform.flip(frame,True,False))
        self.jump_frames_r = pygame.image.load("resources/image/player/jump.png").convert()
        self.jump_frames_l = pygame.transform.flip(self.jump_frames_r,True,False)
        self.climb_frames = [pygame.image.load("resources/image/player/climb_1.png").convert(),pygame.image.load("resources/image/player/climb_2.png").convert(),pygame.image.load("resources/image/player/climb_3.png").convert()]
        self.hurt_frames_r = pygame.image.load("resources/image/player/hurt.png").convert()
        self.hurt_frames_l = pygame.transform.flip(self.hurt_frames_r,True,False)

        self.game = game
        pygame.sprite.Sprite.__init__(self)
        self.image = self.stand_frames_r
        self.image = pygame.transform.scale(self.image,(30,40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, TILE_H*28)
        self.pos = vec(WIDTH/2, TILE_H*28)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.isClimbing = False
        self.isJumpAvaliable = False
        self.isWalking = False
        self.climbedLadder = []
        self.isDead = False
        self.current_frame = 0
        self.last_update = 0
        self.runClimbAnimation = False
        self.isLeft = False

    def update(self):
        self.animate()
        self.runClimbAnimation = False
        keys = pygame.key.get_pressed()

        if not self.isClimbing:
            self.acc = vec(0, PLAYER_GRAV)

            if keys[pygame.K_LEFT]:
                self.acc.x = -PLAYER_ACC
                self.isLeft = True
            if keys[pygame.K_RIGHT]:
                self.acc.x = PLAYER_ACC
                self.isLeft = False
        else:
            self.acc = vec(0, 0)
            #checking for dropdown after climbing action
            if self.rect.centery >  self.climbedLadder.ladderGroup[1] and self.rect.bottom < self.climbedLadder.ladderGroup[0]+5:
                if keys[pygame.K_UP]:
                    self.runClimbAnimation = True
                    self.pos.y += -5
                if keys[pygame.K_DOWN]:
                    self.runClimbAnimation = True
                    self.pos.y += 5
            else:
                self.isClimbing = False

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        #apply air resistance
        self.acc.y += self.vel.y * PLAYER_AIRRESISTANCE
        # equation of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

        if self.rect.top > HEIGHT:
            self.playerDied()

    def jump(self):
        
        if self.isJumpAvaliable:
            self.rect.x += 8
            hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
            self.rect.x -= 8
            if hits or self.isClimbing:
                self.isClimbing = False
                self.vel.y = -16

            self.isJumpAvaliable = False

    def climb(self):

        hits = pygame.sprite.spritecollide(self, self.game.ladders, False)

        if hits:
            self.isClimbing = True
            self.isJumpAvaliable = True
            self.vel = vec(0, 0)
            self.climbedLadder = hits[0]
            self.pos.x = self.climbedLadder.rect.centerx

    def playerDied(self):
        if self.isLeft:
            self.image = self.hurt_frames_l
        else:
            self.image = self.hurt_frames_r
        bottom = self.rect.bottom
        left = self.rect.left
        self.image = pygame.transform.scale(self.image,(30,40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = bottom
        self.rect.left = left
        self.isDead = True

    def reLocate(self, x, y):
        self.rect.center = (x, y)
        self.pos = vec(x, y)

    def animate(self):
        if self.vel.x != 0:
            self.isWalking = True
        else:
            self.isWalking = False
        now = pygame.time.get_ticks()
        if self.isClimbing and self.runClimbAnimation:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) %len(self.climb_frames)
                bottom = self.rect.bottom
                left = self.rect.left
                self.image = self.climb_frames[self.current_frame]
                self.image = pygame.transform.scale(self.image,(30,40))
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                self.rect.left = left
        
        elif not self.isJumpAvaliable:
            if self.vel.x >= 0:
                self.image = self.jump_frames_r
            else:
                self.image = self.jump_frames_l
            
            bottom = self.rect.bottom
            left = self.rect.left
            self.image = pygame.transform.scale(self.image,(30,40))
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
            self.rect.left = left
        elif self.isWalking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) %len(self.run_frames_r)
                bottom = self.rect.bottom
                left = self.rect.left
                if self.vel.x > 0:
                    self.image = self.run_frames_r[self.current_frame]
                else:
                    self.image = self.run_frames_l[self.current_frame]
                self.image = pygame.transform.scale(self.image,(30,40))
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                self.rect.left = left
        elif not self.isWalking and self.isJumpAvaliable and not self.isClimbing:
            if self.isLeft:
                self.image = self.stand_frames_l
            else:
                self.image = self.stand_frames_r
            bottom = self.rect.bottom
            left = self.rect.left
            self.image = pygame.transform.scale(self.image,(30,40))
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
            self.rect.left = left
