
import sys
sys.path.insert(1, '../enemy/')
sys.path.insert(1, '../environment/')
sys.path.insert(1, '../player/')
sys.path.insert(1, '../../')

from robot import Robot
from ladder import Ladder
from coin import Coin
from platform import Platform
from guided_missile import Guided_Missile
from player import Player
from settings import *
from re import match


def createLevel(game, levelIndex):
    platform = []
    ladder = []
    coi = []
    
    game.player = Player(game)

    if levelIndex == 1:
        platform = [(TILE_W*3, HEIGHT-40, WIDTH-TILE_W*6, TILE_H), (TILE_W*5, TILE_H*18, TILE_W*13,
                                                                    TILE_H), (TILE_W*22, TILE_H*18, TILE_W*13, TILE_H), (TILE_W*9, TILE_H*8, TILE_W*22, TILE_H)]
        ladder = [(TILE_W*6, TILE_H*17, TILE_H*11), (TILE_W*33,
                                                     TILE_H*17, TILE_H*11), (TILE_W*31, TILE_H*7, TILE_H*11)]
        coi = [(TILE_W*9, TILE_H*26, game.player), (TILE_W*30, TILE_H*26, game.player), (TILE_W*14,
                                                                                         TILE_H*16, game.player), (TILE_W*25, TILE_H*16, game.player), (TILE_W*14, TILE_H*6, game.player)]

        g1 = Guided_Missile(game.player, 50, -50)
        game.guided_missiles.add(g1)

        game.spawner.restartVariables()
        game.spawner.mMax = 10
        game.spawner.mSpawnTime = 10

    elif levelIndex == 2:
        platform = [(TILE_W*5, HEIGHT-TILE_H*2, TILE_W*12, TILE_H), (TILE_W*23, TILE_H*28, TILE_W*12, TILE_H), (TILE_W*8, TILE_H*18, TILE_W*7,
                                                                                                                TILE_H), (TILE_W*25, TILE_H*18, TILE_W*7, TILE_H), (TILE_W*30, TILE_H*13, TILE_W*5, TILE_H), (TILE_W*10, TILE_H*8, TILE_W*5, TILE_H)]
        ladder = [(TILE_W*19.5, TILE_H*3, TILE_H*22)]
        coi = [(TILE_W*30, TILE_H*26, game.player), (TILE_W*10, TILE_H*16, game.player), (TILE_W*27,
                                                                                          TILE_H*16, game.player), (TILE_W*32, TILE_H*8, game.player), (TILE_W*12, TILE_H*6, game.player)]

        game.player.reLocate(TILE_W*13, TILE_H*25)

        game.spawner.restartVariables()
        game.spawner.gmMax = 5
        game.spawner.gmSpawnTime = 10

    elif levelIndex == 3:
        platform = [(TILE_W*4, HEIGHT-TILE_H*2, TILE_W*32, TILE_H), (TILE_W*15, TILE_H*24, TILE_W*10, TILE_H), (TILE_W*17, TILE_H*21, TILE_W*6, TILE_H), (TILE_W*18, TILE_H*19, TILE_W*4, TILE_H), (TILE_W*2,
                                                                                                                                                                                                    TILE_H*17, TILE_W*14, TILE_H), (TILE_W*23, TILE_H*17, TILE_W*14, TILE_H), (TILE_W*4, TILE_H*10, TILE_W*14, TILE_H), (TILE_W*21, TILE_H*10, TILE_W*14, TILE_H), (TILE_W*8, TILE_H*4, TILE_W*22, TILE_H)]
        ladder = [(TILE_W*8, TILE_H*9, TILE_H*8), (TILE_W*29,
                                                   TILE_H*9, TILE_H*8), (TILE_W*13, TILE_H*3, TILE_H*7)]
        coi = [(TILE_W*28, TILE_H*19, game.player), (TILE_W*14, TILE_H*13, game.player), (TILE_W*19, TILE_H*13, game.player), (TILE_W*4,
                                                                                                                               TILE_H*8, game.player), (TILE_W*19, TILE_H*7, game.player), (TILE_W*34, TILE_H*7, game.player), (TILE_W*26, TILE_H, game.player)]

        r1 = Robot(game, TILE_W*10, TILE_H*7)
        game.robots.add(r1)

        r2 = Robot(game, TILE_W*32, TILE_H*14)
        game.robots.add(r2)

        game.spawner.restartVariables()
    elif levelIndex == 4:
        platform = [(0, HEIGHT-TILE_H*2, WIDTH, TILE_H), (TILE_W*8, TILE_H*16, TILE_W*24, TILE_H),
                    (TILE_W*22, TILE_H*11, TILE_W*14, TILE_H), (TILE_W*5, TILE_H*8, TILE_W*14, TILE_H)]
        ladder = [(TILE_W*12, TILE_H*15, TILE_H*13),
                  (TILE_W*27, TILE_H*15, TILE_H*13)]
        coi = [(TILE_W*18, TILE_H*18, game.player), (TILE_W*34, TILE_H*18, game.player), (TILE_W, TILE_H*12, game.player),
               (TILE_W*16, TILE_H*11, game.player), (TILE_W*33, TILE_H*7, game.player), (TILE_W*8, TILE_H*4, game.player)]

        game.spawner.restartVariables()
        game.spawner.bMax = 50
        game.spawner.bSpawnTime = 20
    else:
        platform = [(TILE_W*10, HEIGHT-TILE_H*2, TILE_W*20, TILE_H), (TILE_W*7, TILE_H*23, TILE_W*5, TILE_H),
                    (TILE_W*28, TILE_H*23, TILE_W*5, TILE_H), (TILE_W*12, TILE_H*19, TILE_W*4, TILE_H), (TILE_W*24, TILE_H*18, TILE_W*4, TILE_H), (TILE_W*7, TILE_H*16, TILE_W*4, TILE_H), (TILE_W*19, TILE_H*14, TILE_W*4, TILE_H), (TILE_W*29, TILE_H*14, TILE_W*4, TILE_H), (TILE_W*3, TILE_H*12, TILE_W*3, TILE_H), (TILE_W*13, TILE_H*12, TILE_W*3, TILE_H), (TILE_W*28, TILE_H*11, TILE_W*3, TILE_H), (TILE_W*19, TILE_H*10, TILE_W*3, TILE_H), (TILE_W*7, TILE_H*8, TILE_W*3, TILE_H), (TILE_W*14, TILE_H*8, TILE_W*3, TILE_H), (TILE_W*25, TILE_H*8, TILE_W*3, TILE_H), (TILE_W*32, TILE_H*8, TILE_W*3, TILE_H), (TILE_W*18, TILE_H*4, TILE_W*5, TILE_H)]
        coi = [(TILE_W*7, TILE_H*20, game.player), (TILE_W*19, TILE_H*18, game.player), (TILE_W*32, TILE_H*20, game.player),
               (TILE_W*15, TILE_H*16, game.player), (TILE_W*32, TILE_H*12, game.player), (TILE_W*24, TILE_H*11, game.player), (TILE_W*3, TILE_H*9, game.player), (TILE_W*20, TILE_H*8, game.player), (TILE_W*33, TILE_H*5, game.player), (TILE_W*19, TILE_H, game.player)]

        game.spawner.restartVariables()
        game.spawner.lbMax = 50
        game.spawner.lbSpawnTime = 25

    for plat in platform:
        p = Platform(*plat)
        game.platforms.add(p)

    for lad in ladder:
        l = Ladder(*lad)
        game.ladders.add(l)

    for coin in coi:
        c = Coin(*coin)
        game.coins.add(c)

    # add sprites to group by draw depth
    game.all_sprites.add(*game.platforms)
    game.all_sprites.add(*game.ladders)
    game.all_sprites.add(*game.coins)
    game.all_sprites.add(*game.guided_missiles)
    game.all_sprites.add(*game.robots)
    game.all_sprites.add(game.player)
