import pygame
from config.settings import *

class Camera:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def update(self, player_rect):
        self.x = player_rect.x + player_rect.width/2 - SCREEN_WIDTH/2
        self.y = player_rect.y + player_rect.height/2 - SCREEN_HEIGHT/2
