import pygame
import sys
sys.path.insert(1,'sprites/enemy/')
sys.path.insert(1,'sprites/environment/')
sys.path.insert(1,'sprites/player/')
sys.path.insert(1,'sprites/misc/')
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
from bomb import Bomb
from laser_beam import LaserBeam


dif = ["EASY", "NORMAL", "HARD"]


class Game:
    def __init__(self):
        # init
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("JumpMan")
        self.clock = pygame.time.Clock()
        self.difficulty = 2
        self.running = True
        self.level = 1
        self.mainMenu = True
        self.selectLevel = False
        self.options = False
        self.clicked = False
        self.health = 3
        self.inGameOver = False
        self.gameOverDelay = 420
        self.current_gameOverDelay = self.gameOverDelay

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.ladders = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.missiles = pygame.sprite.Group()
        self.guided_missiles = pygame.sprite.Group()
        self.robots = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        self.laser_beams = pygame.sprite.Group()
        self.spawner = Spawner(self)
        pygame.time.set_timer(pygame.USEREVENT, 200)
        
        self.run()

    def run(self):

        self.playing = True
        while self.playing:

            self.clock.tick(FPS)
            
            self.clicked = False
            self.events()
            if self.mainMenu:
                self.show_start_screen()

            elif self.inGameOver:
                if self.current_gameOverDelay  <= 0:
                    self.inGameOver = False
                    self.changeHealth()
                    self.level = 1
                    createLevel(self, self.level)
                else:
                    self.current_gameOverDelay  -= 1
                    self.show_go_screen(50+(30*(self.gameOverDelay - self.current_gameOverDelay)/(self.gameOverDelay-1)))

            else:
                self.update()
                self.draw()

    def update(self):

        if self.player.vel.y > 0 :
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
    
            if hits and self.player.pos.y <= hits[0].rect.centery:
                self.player.pos.y = hits[0].rect.top+1
                self.player.vel.y = 0
                self.player.isJumpAvaliable = True

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
            if self.level < 5:
                self.level += 1

                for sprite in self.all_sprites:
                    sprite.kill()

                createLevel(self, self.level)

        #check death
        if self.player.isDead:
            effect = pygame.mixer.Sound('resources/sound/hurt.mp3')
            effect.play()
            pygame.time.delay(500)
            for sprite in self.all_sprites:
                sprite.kill()

            createLevel(self, self.level)
            self.health -= 1
            if self.health <= 0:
                self.current_gameOverDelay = self.gameOverDelay
                effect = pygame.mixer.Sound('resources/sound/GAMEOVER.mp3')
                effect.play()
                for sprite in self.all_sprites:
                    sprite.kill()
                self.inGameOver = True
        
        self.all_sprites.update()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if self.mainMenu:
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    self.clicked = True
            elif self.inGameOver:
                pass
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.jump()
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        self.player.climb()
                    if event.key == pygame.K_ESCAPE:
                        for sprite in self.all_sprites:
                            sprite.kill()
                        
                        self.inGameplay = False
                        self.mainMenu = True

                if event.type == pygame.USEREVENT:
                    self.spawner.current_gmSpawnTime -= 1
                    self.spawner.current_mSpawnTime -= 1
                    self.spawner.current_bSpawnTime -= 1
                    self.spawner.current_lbSpawnTime -= 1
                    if self.spawner.current_gmSpawnTime <= 0:
                        self.spawner.spawnGM()
                    if self.spawner.current_mSpawnTime <= 0:
                        self.spawner.spawnM()
                    if self.spawner.current_bSpawnTime <= 0:
                        self.spawner.spawnB()
                    if self.spawner.current_lbSpawnTime <= 0:
                        self.spawner.spawnLB()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        
        #Health UI
        pygame.draw.rect(self.screen,RED,[TILE_W,TILE_H,TILE_W,TILE_H])
        self.draw_text("X"+str(self.health), 'arial', 25, WHITE, TILE_W*3, TILE_H*0.7)

        # after drawing everything
        pygame.display.flip()

    def show_start_screen(self):
        mouse = pygame.mouse.get_pos()
        self.screen.fill(BLACK)
        
        if self.selectLevel:
            self.select_level(mouse)
        elif self.options:
            self.options_(mouse)
        else:
            self.main_menu(mouse)
        
        pygame.display.flip()

    def show_go_screen(self,size):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER",'arial',int(size),DARKRED,WIDTH/2,HEIGHT/4)
        pygame.display.flip()

    def main_menu(self, mouse):
        self.draw_text("JUMPMAN", 'comicsansms', 50, LOGO, WIDTH/2, HEIGHT/4)
        
        #START button
        pygame.draw.rect(self.screen,WHITE,[WIDTH/2-95,HEIGHT/2-5,190,50]) 
        if WIDTH/2-90 <= mouse[0] <= WIDTH/2+90 and HEIGHT/2 <= mouse[1] <= HEIGHT/2+40: 
            pygame.draw.rect(self.screen,BUTTON_LIGHT,[WIDTH/2-90,HEIGHT/2,180,40]) 
            if self.clicked:
                self.level = 1
                self.mainMenu =False
                self.inGameplay = True
                self.changeHealth()
                createLevel(self, self.level)
        else: 
            pygame.draw.rect(self.screen,BUTTON_DARK,[WIDTH/2-90,HEIGHT/2,180,40])
        self.draw_text("START", 'arial', 25, WHITE, WIDTH/2-5, HEIGHT/2+5)

        #Select Level Button
        pygame.draw.rect(self.screen,WHITE,[WIDTH/2-95,HEIGHT/2+65,190,50]) 
        if WIDTH/2-90 <= mouse[0] <= WIDTH/2+90 and HEIGHT/2+70 <= mouse[1] <= HEIGHT/2+110: 
            pygame.draw.rect(self.screen,BUTTON_LIGHT,[WIDTH/2-90,HEIGHT/2+70,180,40]) 
            if self.clicked:
                self.selectLevel = True
        else: 
            pygame.draw.rect(self.screen,BUTTON_DARK,[WIDTH/2-90,HEIGHT/2+70,180,40])
        self.draw_text("SELECT LEVEL", 'arial', 25, WHITE, WIDTH/2-5, HEIGHT/2+75)

        #Options button
        pygame.draw.rect(self.screen,WHITE,[WIDTH/2-95,HEIGHT/2+135,190,50]) 
        if WIDTH/2-90 <= mouse[0] <= WIDTH/2+90 and HEIGHT/2 +140<= mouse[1] <= HEIGHT/2+180: 
            pygame.draw.rect(self.screen,BUTTON_LIGHT,[WIDTH/2-90,HEIGHT/2+140,180,40]) 
            if self.clicked:
                self.options = True
        else: 
            pygame.draw.rect(self.screen,BUTTON_DARK,[WIDTH/2-90,HEIGHT/2+140,180,40])
        self.draw_text("OPTIONS", 'arial', 25, WHITE, WIDTH/2-5, HEIGHT/2+145)

    def select_level(self, mouse):
        self.draw_text("SELECT A LEVEL", 'comicsansms', 50, WHITE, WIDTH/2, HEIGHT/6)

        for i in range(5):
            pygame.draw.rect(self.screen,WHITE,[160+i*100,250,70,70]) 
            if 165+i*100 <= mouse[0] <= 225+i*100 and 250<= mouse[1] <= 310: 
                pygame.draw.rect(self.screen,BUTTON_LIGHT,[165+i*100,255,60,60]) 
                if self.clicked:
                    self.level = i+1
                    self.mainMenu = False
                    self.inGameplay = True
                    self.changeHealth()
                    createLevel(self, self.level)
            else: 
                pygame.draw.rect(self.screen,BUTTON_DARK,[165+i*100,255,60,60])
            self.draw_text(str(i+1), 'arial', 25, WHITE, 195+i*100, 270)

        pygame.draw.rect(self.screen,WHITE,[550,500,100,50]) 
        if 555 <= mouse[0] <= 655 and 505<= mouse[1] <= 555: 
            pygame.draw.rect(self.screen,BUTTON_LIGHT,[555,505,90,40]) 
            if self.clicked:
                self.selectLevel = False
        else: 
            pygame.draw.rect(self.screen,BUTTON_DARK,[555,505,90,40])
        self.draw_text("BACK", 'arial', 25, WHITE, 600, 510)

    def options_(self, mouse):
        self.draw_text("SELECT A DIFFICULTY", 'comicsansms', 50, WHITE, WIDTH/2, HEIGHT/6)

        for i in range(3):
            pygame.draw.rect(self.screen,WHITE,[140+i*200,250,140,70]) 
            if (145+i*200 <= mouse[0] <= 275+i*200 and 250<= mouse[1] <= 310) or i+1 == self.difficulty: 
                pygame.draw.rect(self.screen,BUTTON_LIGHT,[145+i*200,255,130,60]) 
                if self.clicked:
                    self.difficulty = i+1
            else: 
                pygame.draw.rect(self.screen,BUTTON_DARK,[145+i*200,255,130,60])
            self.draw_text(dif[i], 'arial', 25, WHITE, 210+i*200, 270)

        pygame.draw.rect(self.screen,WHITE,[550,500,100,50]) 
        if 555 <= mouse[0] <= 655 and 505<= mouse[1] <= 555: 
            pygame.draw.rect(self.screen,BUTTON_LIGHT,[555,505,90,40]) 
            if self.clicked:
                self.options = False
        else: 
            pygame.draw.rect(self.screen,BUTTON_DARK,[555,505,90,40])
        self.draw_text("BACK", 'arial', 25, WHITE, 600, 510)

    def draw_text(self, text, font, size, color, x, y):
        pygame.font.init()
        font = pygame.font.SysFont(font, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def changeHealth(self):
        if self.difficulty == 1:
            self.health = 5
        elif self.difficulty == 2:
            self.health = 3
        else:
            self.health = 1
