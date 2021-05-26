from settings import *
from re import match
from missile import Missile
from guided_missile import Guided_Missile
from platform import Platform
from coin import Coin
from ladder import Ladder

def createLevel(game, levelIndex):
    platform = []
    ladder = []
    coi = []

    if levelIndex == 1:
        platform = [(TILE_W*3, HEIGHT-40, WIDTH-TILE_W*6, TILE_H),(TILE_W*5, TILE_H*18, TILE_W*13, TILE_H),(TILE_W*22, TILE_H*18, TILE_W*13, TILE_H),(TILE_W*9, TILE_H*8, TILE_W*22, TILE_H)]
        ladder = [(TILE_W*6, TILE_H*17, TILE_H*11),(TILE_W*33, TILE_H*17, TILE_H*11),(TILE_W*31, TILE_H*7, TILE_H*11)]
        coi = [(TILE_W*9, TILE_H*26, game.player),(TILE_W*30, TILE_H*26, game.player),(TILE_W*14, TILE_H*16, game.player),(TILE_W*25, TILE_H*16, game.player),(TILE_W*14, TILE_H*6, game.player)]
        
        m1 = Missile(game.player)
        game.missiles.add(m1)

        g1 = Guided_Missile(game.player)
        game.guided_missiles.add(g1)

    for plat in platform:
            p = Platform(*plat)
            game.platforms.add(p)

    for lad in ladder:
        l = Ladder(*lad)
        game.ladders.add(l)

    for coin in coi:
        c = Coin(*coin)
        game.coins.add(c)

    #add sprites to group by draw depth
    game.all_sprites.add(*game.platforms)
    game.all_sprites.add(*game.ladders)
    game.all_sprites.add(*game.coins)
    game.all_sprites.add(*game.missiles)
    game.all_sprites.add(*game.guided_missiles)
    game.all_sprites.add(game.player)



