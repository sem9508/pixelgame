import pygame
from config.colors import *
from config.settings import *
import random

class Enemy:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = TILE_SIZE - ENEMY_TILE_OFFSET*2
        self.height = TILE_SIZE - ENEMY_TILE_OFFSET*2
        self.img = pygame.image.load('./assets/enemy.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, (self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def follow_player(self, player_x, player_y):
        # Simple AI to follow the player based on their world position
        if player_x < self.x:
            self.x -= self.speed
        elif player_x > self.x:
            self.x += self.speed
        if player_y < self.y:
            self.y -= self.speed
        elif player_y > self.y:
            self.y += self.speed

    def draw(self, screen, camera_x_offset, camera_y_offset):
        adjusted_x = self.x - camera_x_offset
        adjusted_y = self.y - camera_y_offset
        if (adjusted_x + self.width > 0 and adjusted_x < SCREEN_WIDTH and 
            adjusted_y + self.height > 0 and adjusted_y < SCREEN_HEIGHT):
            screen.blit(self.img, (adjusted_x, adjusted_y))

    def update(self, player_x, player_y):
        self.follow_player(player_x, player_y)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
