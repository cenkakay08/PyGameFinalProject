import pygame
import sys
sys.path.insert(1,'../enemy/')
from settings import *
from guided_missile import Guided_Missile
import random
from missile import Missile
from bomb import Bomb


class Spawner(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.gmSpawnTime = 10
        self.current_gmSpawnTime = 0
        self.mSpawnTime = 10
        self.current_mSpawnTime = 0
        self.bSpawnTime = 10
        self.current_bSpawnTime = 0
        self.lbSpawnTime = 10
        self.current_lbSpawnTime = 0
        self.gmMax = 1
        self.mMax = 1
        self.bMax = 1
        self.lbMax = 1

    def spawnGM(self):
        if self.gmMax > 0:
            g1 = Guided_Missile(self.game.player,random.randint(50, WIDTH-50),-50)
            self.game.guided_missiles.add(g1)
            self.game.all_sprites.add(g1)
            self.gmMax -= 1
        self.current_gmSpawnTime = self.gmSpawnTime

    def spawnM(self):
        if self.mMax > 0:
            m1 = Missile(self.game.player)
            self.game.missiles.add(m1)
            self.game.all_sprites.add(m1)
            self.mMax -= 1

        self.current_mSpawnTime = self.mSpawnTime

    def spawnB(self):
        if self.bMax > 0:
            b1 = Missile(self.game.player)
            self.game.bombs.add(b1)
            self.game.all_sprites.add(b1)
            self.bMax -= 1

        self.current_bSpawnTime = self.bSpawnTime

    def spawnLB(self):
        if self.lbMax > 0:
            lb1 = Missile(self.game.player)
            self.game.laser_beams.add(lb1)
            self.game.all_sprites.add(lb1)
            self.lbMax -= 1

        self.current_lbSpawnTime = self.lbSpawnTime