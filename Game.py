import pygame
from settings import *
from levels import *
from player import Player
from platform import Platform
from ladder import Ladder
from coin import Coin
from missile import Missile
from guided_missile import Guided_Missile


class Game:
    def __init__(self):
        # init
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("JumpMan")
        self.clock = pygame.time.Clock()
        self.running = True

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.ladders = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.missiles = pygame.sprite.Group()
        self.guided_missiles = pygame.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        
        for plat in LEVELS[0][0]:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)

        for lad in LEVELS[0][1]:
            l = Ladder(*lad)
            self.all_sprites.add(l)
            self.ladders.add(l)

        for coin in LEVELS[0][2]:
            c = Coin(coin[0],coin[1],self.player)
            self.all_sprites.add(c)
            self.coins.add(c)

        m1 = Missile(self.player)
        self.all_sprites.add(m1)
        self.missiles.add(m1)

        g1 = Guided_Missile(self.player)
        self.all_sprites.add(g1)
        self.guided_missiles.add(g1)

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
    
            if hits:
                self.player.pos.y = hits[0].rect.top+1
                self.player.vel.y = 0

        #remove picked coins
        for coin in self.coins:
            if coin.isPicked:
                self.all_sprites.remove(coin)
                self.coins.remove(coin)

        #remove missiles out of screen
        for missile in self.missiles:
            if missile.rect.top > HEIGHT:
                self.all_sprites.remove(missile)
                self.missiles.remove(missile)

        #remove guided missiles out of screen
        for guided_missile in self.guided_missiles:
            if guided_missile.rect.top > HEIGHT or guided_missile.rect.left > WIDTH:
                self.all_sprites.remove(guided_missile)
                self.guided_missiles.remove(guided_missile)

        #check win
        if len(self.coins) == 0:
            #YOU WON
            None
        

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

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        # after drawing everything
        pygame.display.flip()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass
