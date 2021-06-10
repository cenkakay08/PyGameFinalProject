import pygame

from settings import *
from sprites.misc.levels import *
from sprites.player.player import Player
from sprites.environment.platform import Platform
from sprites.environment.ladder import Ladder
from sprites.environment.coin import Coin
from sprites.enemy.missile import Missile
from sprites.enemy.guided_missile import Guided_Missile
from sprites.misc.spawner import Spawner
from sprites.enemy.robot import Robot
from sprites.enemy.bomb import Bomb
from sprites.enemy.laser_beam import LaserBeam
from sprites.enemy.boss import Boss
from sprites.environment.one_up import One_Up

dif = ["EASY", "NORMAL", "HARD"]

class Game:
    def __init__(self):
        # init
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("JumpMan")
        self.hearth_frame = pygame.image.load("resources/image/misc/hearth.png").convert_alpha()
        self.background_frames = [pygame.image.load("resources/image/misc/background_1.png").convert_alpha(),
                                  pygame.image.load("resources/image/misc/background_2.png").convert_alpha(),
                                  pygame.image.load("resources/image/misc/background_3.png").convert_alpha(),
                                  pygame.image.load("resources/image/misc/background_4.png").convert_alpha(),
                                  pygame.image.load("resources/image/misc/background_5.png").convert_alpha()]
        self.hearth_frame = pygame.transform.scale(self.hearth_frame, (TILE_W, TILE_H))
        self.clock = pygame.time.Clock()
        self.difficulty = 2
        self.running = True
        self.level = 1
        self.mainMenu = True
        self.selectLevel = False
        self.options = False
        self.story = False
        self.clicked = False
        self.health = 3
        self.inGameOver = False
        self.gameOverDelay = 420
        self.current_gameOverDelay = self.gameOverDelay
        self.levelStarted = False
        self.levelInfoDelay = 200
        self.current_levelInfoDelay = self.levelInfoDelay
        # Story fadeout Variables
        self.fadeoutTime = 100
        self.current_fadeoutTime = 0
        self.storyDelay = 1000
        self.current_storyDelay = 0
        self.startingStoryScenes = 3
        self.current_startingStoryScenes = 0
        self.endingStoryScenes = 1
        self.current_endingStoryScenes = 0
        self.isFadingOut = False

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
        self.one_ups = pygame.sprite.Group()
        self.spawner = Spawner(self)
        pygame.time.set_timer(pygame.USEREVENT, 200)
        self.musicPlayed = False

        self.run()

    def run(self):

        self.playing = True
        while self.playing:

            self.clock.tick(FPS)

            self.clicked = False
            self.events()
            if self.story:

                self.playMusic("story")
                self.story_squence()

            elif self.mainMenu:
                self.playMusic("menu")

                self.show_start_screen()

            elif self.inGameOver:
                self.show_go_screen()

            elif self.levelStarted:
                pygame.mixer.music.fadeout(800)
                self.level_info_screen()


            else:

                if self.level == 6:
                    self.playMusic("boss")
                else:
                    self.playMusic("game")

                self.update()
                self.draw()

    def update(self):

        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)

            if hits and self.player.pos.y <= hits[0].rect.centery:
                self.player.pos.y = hits[0].rect.top + 1
                self.player.vel.y = 0
                self.player.isJumpAvaliable = True

        # check win
        if len(self.coins) == 0:
            pygame.mixer.music.fadeout(500)
            effect = pygame.mixer.Sound('resources/sound/victory.wav')
            effect.play()
            pygame.time.delay(4500)
            if self.level < 6:
                self.level += 1

                self.killAllSprites()

                self.levelStarted = True
            else:
                self.story = True
                self.musicPlayed = False
                self.mainMenu = True
                self.selectLevel = False

        # check death
        if self.player.isDead:
            pygame.time.delay(500)
            self.killAllSprites()

            self.health -= 1
            if self.health <= 0:
                self.current_gameOverDelay = self.gameOverDelay
                effect = pygame.mixer.Sound('resources/sound/GAMEOVER.ogg')
                effect.play()
                self.killAllSprites()
                self.inGameOver = True
            else:
                createLevel(self, self.level)

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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.killAllSprites()

                        self.inGameplay = False
                        self.mainMenu = True
                        self.inGameOver = False
                        pygame.mixer.stop()
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.jump()
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        self.player.climb()
                    if event.key == pygame.K_ESCAPE:
                        self.killAllSprites()

                        self.inGameplay = False
                        self.selectLevel = False
                        self.options = False
                        self.mainMenu = True
                        self.musicPlayed = False

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
        # draw background
        for frame in self.background_frames:
            image = pygame.transform.scale(frame, (WIDTH, HEIGHT))
            self.screen.blit(image, (0, 0))
        self.all_sprites.draw(self.screen)

        # Health UI
        self.screen.blit(self.hearth_frame, (TILE_W, TILE_H))
        self.draw_text("X" + str(self.health), 'arial', 25, WHITE, TILE_W * 3, TILE_H * 0.7, 255)

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

    def show_go_screen(self):
        if self.current_gameOverDelay <= 0:
            self.inGameOver = False
            self.changeHealth()
            self.level = 1
            self.levelStarted = True
        else:
            self.current_gameOverDelay -= 1
            self.screen.fill(BLACK)
            self.draw_text("YOU DIED", 'arial', int(
                50 + (30 * (self.gameOverDelay - self.current_gameOverDelay) / (self.gameOverDelay - 1))), DARKRED,
                           WIDTH / 2, HEIGHT / 4,
                           255 * (self.gameOverDelay - self.current_gameOverDelay) / (self.gameOverDelay - 1))
            pygame.display.flip()

    def main_menu(self, mouse):
        self.draw_text("JUMPMAN", 'comicsansms', 50, LOGO, WIDTH / 2, HEIGHT / 4, 255)

        # START button
        pygame.draw.rect(self.screen, WHITE, [WIDTH / 2 - 95, HEIGHT / 2 - 5, 190, 50])
        if WIDTH / 2 - 90 <= mouse[0] <= WIDTH / 2 + 90 and HEIGHT / 2 <= mouse[1] <= HEIGHT / 2 + 40:
            pygame.draw.rect(self.screen, BUTTON_LIGHT, [WIDTH / 2 - 90, HEIGHT / 2, 180, 40])
            if self.clicked:
                self.level = 1
                self.mainMenu = False
                self.story = True
                self.musicPlayed = False
                self.inGameplay = True
                self.changeHealth()
                self.levelStarted = True
        else:
            pygame.draw.rect(self.screen, BUTTON_DARK, [WIDTH / 2 - 90, HEIGHT / 2, 180, 40])
        self.draw_text("START", 'arial', 25, WHITE, WIDTH / 2 - 5, HEIGHT / 2 + 5, 255)

        # Select Level Button
        pygame.draw.rect(self.screen, WHITE, [WIDTH / 2 - 95, HEIGHT / 2 + 65, 190, 50])
        if WIDTH / 2 - 90 <= mouse[0] <= WIDTH / 2 + 90 and HEIGHT / 2 + 70 <= mouse[1] <= HEIGHT / 2 + 110:
            pygame.draw.rect(self.screen, BUTTON_LIGHT, [WIDTH / 2 - 90, HEIGHT / 2 + 70, 180, 40])
            if self.clicked:
                self.selectLevel = True
        else:
            pygame.draw.rect(self.screen, BUTTON_DARK, [WIDTH / 2 - 90, HEIGHT / 2 + 70, 180, 40])
        self.draw_text("SELECT LEVEL", 'arial', 25, WHITE, WIDTH / 2 - 5, HEIGHT / 2 + 75, 255)

        # Options button
        pygame.draw.rect(self.screen, WHITE, [WIDTH / 2 - 95, HEIGHT / 2 + 135, 190, 50])
        if WIDTH / 2 - 90 <= mouse[0] <= WIDTH / 2 + 90 and HEIGHT / 2 + 140 <= mouse[1] <= HEIGHT / 2 + 180:
            pygame.draw.rect(self.screen, BUTTON_LIGHT, [WIDTH / 2 - 90, HEIGHT / 2 + 140, 180, 40])
            if self.clicked:
                self.options = True
        else:
            pygame.draw.rect(self.screen, BUTTON_DARK, [WIDTH / 2 - 90, HEIGHT / 2 + 140, 180, 40])
        self.draw_text("OPTIONS", 'arial', 25, WHITE, WIDTH / 2 - 5, HEIGHT / 2 + 145, 255)

    def select_level(self, mouse):
        self.draw_text("SELECT A LEVEL", 'comicsansms', 50, WHITE, WIDTH / 2, HEIGHT / 6, 255)
        index = 1
        for j in range(2):
            for i in range(3):
                pygame.draw.rect(self.screen, WHITE, [250 + i * 100, 250 + j * 100, 70, 70])
                if 255 + i * 100 <= mouse[0] <= 315 + i * 100 and 250 + j * 100 <= mouse[1] <= 310 + j * 100:
                    pygame.draw.rect(self.screen, BUTTON_LIGHT, [255 + i * 100, 255 + j * 100, 60, 60])
                    if self.clicked:
                        self.level = index
                        self.mainMenu = False
                        self.inGameplay = True
                        self.changeHealth()
                        self.levelStarted = True
                else:
                    pygame.draw.rect(self.screen, BUTTON_DARK, [255 + i * 100, 255 + j * 100, 60, 60])
                self.draw_text(str(index), 'arial', 25, WHITE, 285 + i * 100, 270 + j * 100, 255)
                index += 1

        pygame.draw.rect(self.screen, WHITE, [550, 500, 100, 50])
        if 555 <= mouse[0] <= 655 and 505 <= mouse[1] <= 555:
            pygame.draw.rect(self.screen, BUTTON_LIGHT, [555, 505, 90, 40])
            if self.clicked:
                self.selectLevel = False
        else:
            pygame.draw.rect(self.screen, BUTTON_DARK, [555, 505, 90, 40])
        self.draw_text("BACK", 'arial', 25, WHITE, 600, 510, 255)

    def options_(self, mouse):
        self.draw_text("OPTIONS", 'comicsansms', 50, WHITE, WIDTH / 2, 50, 255)
        self.draw_text("SELECT A DIFFICULTY:", 'arial', 30, WHITE, WIDTH / 4, 150, 255)

        for i in range(3):
            pygame.draw.rect(self.screen, WHITE, [140 + i * 200, 200, 140, 70])
            if (145 + i * 200 <= mouse[0] <= 275 + i * 200 and 200 <= mouse[1] <= 260) or i + 1 == self.difficulty:
                pygame.draw.rect(self.screen, BUTTON_LIGHT, [145 + i * 200, 205, 130, 60])
                if self.clicked:
                    self.difficulty = i + 1
            else:
                pygame.draw.rect(self.screen, BUTTON_DARK, [145 + i * 200, 205, 130, 60])
            self.draw_text(dif[i], 'arial', 25, WHITE, 210 + i * 200, 220, 255)

        pygame.draw.rect(self.screen, WHITE, [550, 500, 100, 50])
        if 555 <= mouse[0] <= 655 and 505 <= mouse[1] <= 555:
            pygame.draw.rect(self.screen, BUTTON_LIGHT, [555, 505, 90, 40])
            if self.clicked:
                self.options = False
        else:
            pygame.draw.rect(self.screen, BUTTON_DARK, [555, 505, 90, 40])
        self.draw_text("BACK", 'arial', 25, WHITE, 600, 510, 255)

        # How to Play
        self.draw_text("HOW TO PLAY:", 'arial', 30, WHITE, WIDTH / 5, 350, 255)
        self.draw_text("WALK:             LEFT and RIGHT KEYS", 'arial', 20, WHITE, WIDTH / 2, 400, 255)
        self.draw_text("JUMP:                               SPACE BAR", 'arial', 20, WHITE, WIDTH / 2, 430, 255)
        self.draw_text("CLIMB:                 UP and DOWN KEYS", 'arial', 20, WHITE, WIDTH / 2, 460, 255)

    def draw_text(self, text, font, size, color, x, y, alpha):
        pygame.font.init()
        font = pygame.font.SysFont(font, size)
        text_surface = font.render(text, True, color)
        text_surface.set_alpha(alpha)
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

    def level_info_screen(self):
        if self.current_levelInfoDelay <= 0:
            self.killAllSprites()
            self.spawner.kill()
            self.spawner = Spawner(self)
            createLevel(self, self.level)
            self.current_levelInfoDelay = self.levelInfoDelay
            self.levelStarted = False
        else:
            self.screen.fill(BLACK)
            self.draw_text("LEVEL " + str(self.level), 'arial', 50, WHITE, WIDTH / 2, HEIGHT / 2, 255)
            pygame.display.flip()
            self.current_levelInfoDelay -= 1

    def story_squence(self):
        self.screen.fill(BLACK)
        startingStory = ["A long time ago in a faraway land lived a brave warrior.",
                         "The Brave Warrior loved a princess who loves him back.",
                         "But the King not respected his bravery. The King only respected the money.",
                         "The Brave Warrior sought Goddess of Fortune, Fortuna.",
                         "Fortuna accepted to make real his wishes with one condition.",
                         "Fortuna showed the old castle to the Brave Warrior.",
                         "Told him monster Skull inside the castle stole his precious coins.",
                         "Fortuna told the Brave Warrior, who enters the castle cannot use his sword.",
                         "The Brave Warrior pertinaciously enters the castle for his love."]
        endingStory = ["After saving all coins Fortuna bestows him his wish.",
                       "The Brave Warrior with money earns respect of the King.",
                       "The Brave Warrior and the Princess live happily after."]
        text = ""
        alpha = 255

        if self.current_fadeoutTime <= self.fadeoutTime:
            if self.isFadingOut:
                alpha = 255 - (255 * (self.current_fadeoutTime / self.fadeoutTime))
            else:
                alpha = 255 * (self.current_fadeoutTime / self.fadeoutTime)
            self.current_fadeoutTime += 1
        else:
            if self.current_storyDelay >= self.storyDelay:
                self.isFadingOut = True

                self.current_fadeoutTime = 0
                self.current_storyDelay = 0

            else:
                if self.isFadingOut:

                    if self.level == 0:
                        if self.current_startingStoryScenes < self.startingStoryScenes - 1:
                            self.current_startingStoryScenes += 1
                        else:
                            self.story = False
                            self.musicPlayed = False
                    else:
                        if self.current_endingStoryScenes < self.current_endingStoryScenes:
                            self.current_endingStoryScenes += 1
                        else:
                            self.story = False
                            self.musicPlayed = False
                    self.current_fadeoutTime = 0
                    self.isFadingOut = False
                    alpha = 0
                else:
                    self.current_storyDelay += 1

        for i in range(3):
            if self.level == 0:
                text = startingStory[self.current_startingStoryScenes * 3 + i]
            else:
                text = endingStory[self.current_endingStoryScenes * 3 + i]

            self.draw_text(text, 'arial', 25, WHITE, WIDTH / 2, 200 + i * 60, alpha)
        pygame.display.flip()

    def killAllSprites(self):
        for sprite in self.all_sprites:
            sprite.kill()
        for sprite in self.platforms:
            sprite.kill()
        for sprite in self.ladders:
            sprite.kill()
        for sprite in self.coins:
            sprite.kill()
        for sprite in self.missiles:
            sprite.kill()
        for sprite in self.robots:
            sprite.kill()
        for sprite in self.bombs:
            sprite.kill()
        for sprite in self.laser_beams:
            sprite.kill()
        for sprite in self.one_ups:
            sprite.kill()

    def playMusic(self, music):
        if not self.musicPlayed:
            pygame.mixer.music.fadeout(500)
            if music == "game":
                pygame.mixer.music.load("resources/sound/game_music.ogg")
                pygame.mixer.music.play(-1)
            elif music == "menu":
                pygame.mixer.music.load("resources/sound/menu_music.ogg")
                pygame.mixer.music.play(-1)
            elif music == "boss":
                pygame.mixer.music.load("resources/sound/boss_music.ogg")
                pygame.mixer.music.play(-1)
            elif music == "story":
                pygame.mixer.music.load("resources/sound/story_music.ogg")
                pygame.mixer.music.play(-1)
            else:
                print("Something is wrong")

            self.musicPlayed = True
