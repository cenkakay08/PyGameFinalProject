import pygame
from Game import Game


def main():
    g = Game()
    while g.running:
        g.new()
        g.show_go_screen()

    pygame.quit()


if __name__ == "__main__":
    main()
