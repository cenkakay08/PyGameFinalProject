import pygame
from Game import Game


def main():
    g = Game()
    while g.running:
        g.new()

    pygame.quit()

       
if __name__ == "__main__":
    main()
