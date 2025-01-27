import pygame
from config.colors import *
from config.settings import *

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.width = TILE_SIZE - PLAYER_TILE_OFFSET*2
        self.height = TILE_SIZE - PLAYER_TILE_OFFSET*2
        self.speed = PLAYER_SPEED

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x + PLAYER_TILE_OFFSET, self.y + PLAYER_TILE_OFFSET, self.width, self.height))

    def move_x(self, dir):
        self.x += dir*PLAYER_SPEED*TILE_SIZE

    def move_y(self, dir):
        self.y += dir*PLAYER_SPEED*TILE_SIZE