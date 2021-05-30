import pygame
from settings import *
from levels import *
from player import Player
from platform import Platform
from ladder import Ladder
from coin import Coin
from missile import Missile
from guided_missile import Guided_Missile
from spawner import Spawner
from robot import Robot


class Game:
    def __init__(self):
        # init
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("JumpMan")
        self.clock = pygame.time.Clock()
        self.running = True
        self.level = 1

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.ladders = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.missiles = pygame.sprite.Group()
        self.guided_missiles = pygame.sprite.Group()
        self.robots = pygame.sprite.Group()
        self.player = Player(self)
        self.spawner = Spawner(self)
        pygame.time.set_timer(pygame.USEREVENT, 200)
        createLevel(self, self.level)

        r1 = Robot(self, 200, 550)
        self.robots.add(r1)
        self.all_sprites.add(r1)
        
        self.run()

    def run(self):

        self.playing = True
        while self.playing:

            self.clock.tick(FPS)

            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()

        if self.player.vel.y > 0 :
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
    
            if hits and self.player.pos.y <= hits[0].rect.centery:
                self.player.pos.y = hits[0].rect.top+1
                self.player.vel.y = 0

        #remove picked coins
        for coin in self.coins:
            if coin.isPicked:
                coin.kill()

        #remove missiles out of screen
        for missile in self.missiles:
            if missile.rect.top > HEIGHT:
                missile.kill()

        #remove guided missiles out of screen
        for guided_missile in self.guided_missiles:
            if guided_missile.rect.top > HEIGHT or guided_missile.rect.left > WIDTH:
                guided_missile.kill()

        #check win
        if len(self.coins) == 0:
            if self.level < 2:
                self.level += 1

                for sprite in self.all_sprites:
                    sprite.kill()

                self.player = Player(self)

                createLevel(self, self.level)

        #check death
        if self.player.isDead:
            for sprite in self.all_sprites:
                sprite.kill()

            self.player = Player(self)

            createLevel(self, self.level)
        

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.player.climb()

            if event.type == pygame.USEREVENT:
                self.spawner.current_gmSpawnTime -= 1
                self.spawner.current_mSpawnTime -= 1
                if self.spawner.current_gmSpawnTime <= 0:
                    self.spawner.spawnGM()
                if self.spawner.current_mSpawnTime <= 0:
                    self.spawner.spawnM()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        # after drawing everything
        pygame.display.flip()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass
