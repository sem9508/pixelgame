from game import Game
from constants import *
import pygame

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    game = Game(screen)
    game.loop()