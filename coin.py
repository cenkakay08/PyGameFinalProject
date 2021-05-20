import pygame
from settings import *
vec = pygame.math.Vector2


class Coin(pygame.sprite.Sprite):
    def __init__(self, x , y, game):
        self.game = game
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        hits = pygame.sprite.spritecollide(self.game.player, self.game.coins, False)
        if hits:
            self.game.coins.remove(hits[0])
            self.game.all_sprites.remove(hits[0])