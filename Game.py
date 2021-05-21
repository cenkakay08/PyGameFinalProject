import pygame
from settings import *
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
        p1 = Platform(0, HEIGHT-40, WIDTH, 40)
        self.all_sprites.add(p1)
        self.platforms.add(p1)
        p2 = Platform(WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20)
        self.all_sprites.add(p2)
        self.platforms.add(p2)

        l1 = Ladder(WIDTH / 2 - 50, HEIGHT * 1/3, 250)
        self.all_sprites.add(l1)
        self.ladders.add(l1)

        c1 = Coin(110, HEIGHT-80, self.player)
        self.all_sprites.add(c1)
        self.coins.add(c1)

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
        

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                if event.key == pygame.K_UP:
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
