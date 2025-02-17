import pygame
from config.settings import *

class LootBox:
    def __init__(self, world_x, world_y, items):
        self.rect = pygame.Rect(world_x, world_y, TILE_SIZE, TILE_SIZE)
        self.img = pygame.image.load('assets/chest.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, (self.rect.width, self.rect.height))
        self.items = items

    def draw(self, screen, camera):
        screen.blit(self.img, (self.rect.x - camera.x, self.rect.y - camera.y))
