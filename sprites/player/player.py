import pygame
import sys
sys.path.insert(1,'../../')
from settings import *
vec = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.isClimbing = False
        self.isJumpAvaliable = False
        self.climbedLadder = None
        self.isDead = False

    def update(self):
        keys = pygame.key.get_pressed()

        if not self.isClimbing:
            self.acc = vec(0, PLAYER_GRAV)

            if keys[pygame.K_LEFT]:
                self.acc.x = -PLAYER_ACC
            if keys[pygame.K_RIGHT]:
                self.acc.x = PLAYER_ACC
        else:
            self.acc = vec(0, 0)

            #checking for dropdown after climbing action
            if self.rect.centery >  self.climbedLadder.rect.top and self.rect.bottom < self.climbedLadder.rect.bottom+5:
                if keys[pygame.K_UP]:
                    self.pos.y += -5
                if keys[pygame.K_DOWN]:
                    self.pos.y += 5
            else:
                self.isClimbing = False

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        #apply air resistance
        self.acc.y += self.vel.y * PLAYER_AIRRESISTANCE
        # equation of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

        if self.rect.top > HEIGHT:
            self.playerDied()

    def jump(self):
        
        self.rect.x += 8
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 8
        if hits or self.isClimbing:
            self.isClimbing = False
            self.vel.y = -16

    def climb(self):

        hits = pygame.sprite.spritecollide(self, self.game.ladders, False)

        if hits:
            self.isClimbing = True
            self.vel = vec(0, 0)
            self.climbedLadder = hits[0]
            self.pos.x = self.climbedLadder.rect.centerx

    def playerDied(self):
        self.isDead = True

    def reLocate(self, x, y):
        self.rect.center = (x, y)
        self.pos = vec(x, y)
