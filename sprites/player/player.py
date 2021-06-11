import pygame
from settings import *
vec = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        # Load Frames
        self.stand_frames_r = pygame.image.load(
            "resources/image/player/stand.png").convert_alpha()
        self.stand_frames_l = pygame.transform.flip(
            self.stand_frames_r, True, False)
        self.run_frames_r = [pygame.image.load("resources/image/player/run_1.png").convert_alpha(), pygame.image.load("resources/image/player/run_2.png").convert_alpha(), pygame.image.load(
            "resources/image/player/run_3.png").convert_alpha(), pygame.image.load("resources/image/player/run_4.png").convert_alpha(), pygame.image.load("resources/image/player/run_5.png").convert_alpha()]
        self.run_frames_l = []
        for frame in self.run_frames_r:
            self.run_frames_l.append(pygame.transform.flip(frame, True, False))
        self.jump_frames_r = pygame.image.load(
            "resources/image/player/jump.png").convert_alpha()
        self.jump_frames_l = pygame.transform.flip(
            self.jump_frames_r, True, False)
        self.climb_frames = [pygame.image.load("resources/image/player/climb_1.png").convert_alpha(), pygame.image.load(
            "resources/image/player/climb_2.png").convert_alpha(), pygame.image.load("resources/image/player/climb_3.png").convert_alpha()]
        self.hurt_frames_r = pygame.image.load(
            "resources/image/player/hurt.png").convert_alpha()
        self.hurt_frames_l = pygame.transform.flip(
            self.hurt_frames_r, True, False)

        # Load sound effects
        self.hurt_sound = pygame.mixer.Sound('resources/sound/hurt.wav')
        self.jump_sound = pygame.mixer.Sound('resources/sound/jump.wav')

        self.game = game
        pygame.sprite.Sprite.__init__(self)
        self.image = self.stand_frames_r
        self.image = pygame.transform.scale(self.image, (30, 40))
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
        # used this variable to stop animation during waiting on ladder
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
            # checking for dropdown after climbing action
            #climbedLadderGroup used for know when ends when start ladders that connect to each othe
            if self.rect.bottom > self.climbedLadder.ladderGroup[1] and self.rect.bottom < self.climbedLadder.ladderGroup[0]+5:
                if keys[pygame.K_UP]:
                    # as can see if we push bıttons animation starts
                    self.runClimbAnimation = True
                    self.pos.y += -5
                if keys[pygame.K_DOWN]:
                    self.runClimbAnimation = True
                    self.pos.y += 5
            else:
                self.isClimbing = False

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # apply air resistance
        self.acc.y += self.vel.y * PLAYER_AIRRESISTANCE
        # equation of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc

        # don't allow to player go out of screen
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.y < TILE_H:
            self.pos.y = TILE_H

        # rect to realte pos
        self.rect.midbottom = self.pos

        if self.rect.top > HEIGHT:
            self.playerDied()

        if not self.isDead:
            self.animate()

    def jump(self):

        #jump avaliable when charecter stands on platform
        if self.isJumpAvaliable:
            self.jump_sound.play()
            self.rect.x += 8
            hits = pygame.sprite.spritecollide(
                self, self.game.platforms, False)
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
        self.hurt_sound.play()
        if self.isLeft:
            self.image = self.hurt_frames_l
        else:
            self.image = self.hurt_frames_r
        bottom = self.rect.bottom
        left = self.rect.left
        self.image = pygame.transform.scale(self.image, (30, 40))
        self.rect = self.image.get_rect()
        self.rect.bottom = bottom
        self.rect.left = left
        self.isDead = True

    #spawn player or tp it to another location used on second level
    def reLocate(self, x, y):
        self.rect.center = (x, y)
        self.pos = vec(x, y)

    def animate(self):
        #is charecter walking
        if self.vel.x != 0:
            self.isWalking = True
        else:
            self.isWalking = False

        now = pygame.time.get_ticks()

        #if charecter limbing and climbanimation true play animation
        if self.isClimbing and self.runClimbAnimation:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (
                    self.current_frame + 1) % len(self.climb_frames)
                bottom = self.rect.bottom
                left = self.rect.left
                self.image = self.climb_frames[self.current_frame]
                self.image = pygame.transform.scale(self.image, (30, 40))
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                self.rect.left = left
        #if isjump not avaliable means charecter on air
        elif not self.isJumpAvaliable:
            if self.vel.x >= 0:
                self.image = self.jump_frames_r
            else:
                self.image = self.jump_frames_l

            bottom = self.rect.bottom
            left = self.rect.left
            self.image = pygame.transform.scale(self.image, (38, 48))
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
            self.rect.left = left
        #if walking play walk animation
        elif self.isWalking:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (
                    self.current_frame + 1) % len(self.run_frames_r)
                bottom = self.rect.bottom
                left = self.rect.left
                if self.vel.x > 0:
                    self.image = self.run_frames_r[self.current_frame]
                else:
                    self.image = self.run_frames_l[self.current_frame]
                self.image = pygame.transform.scale(self.image, (30, 40))
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                self.rect.left = left
        #if stopped just use idle frame
        elif not self.isWalking and self.isJumpAvaliable and not self.isClimbing:
            if self.isLeft:
                self.image = self.stand_frames_l
            else:
                self.image = self.stand_frames_r
            bottom = self.rect.bottom
            left = self.rect.left
            self.image = pygame.transform.scale(self.image, (30, 40))
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
            self.rect.left = left
        #declare mask for collision with final boss and laser beam
        self.mask = pygame.mask.from_surface(self.image)
