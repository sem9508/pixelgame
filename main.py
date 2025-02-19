from scenes.game import Game
from config.colors import *
from scenes.menu import Menu
from config.settings import *
import pygame
import sys

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init() 

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    active_screen = 0

    while True:
        if active_screen == 0: # GAME
            game = Game(screen)
            active_screen = game.loop()

        elif active_screen == 1: # MENU
            menu = Menu(screen)
            active_screen = menu.loop()

        else: # -1
            break

    pygame.quit()
    sys.exit()