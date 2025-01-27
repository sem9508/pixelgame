from scenes.game import Game
from config.colors import *
from config.settings import *
import pygame

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    game = Game(screen)
    game.loop()