import pygame
from config.colors import *
from config.settings import *
import random
import math

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

    def can_see_player(self, player_rect, chunks):
        # Get the center of the enemy and player
        enemy_center = (self.x + self.width // 2, self.y + self.height // 2)
        player_center = (player_rect.x + player_rect.width // 2, player_rect.y + player_rect.height // 2)

        # Calculate the distance and direction between enemy and player
        dx = player_center[0] - enemy_center[0]
        dy = player_center[1] - enemy_center[1]
        distance = math.hypot(dx, dy)

        if distance == 0:
            return True  # Enemy and player are at the same position

        # Normalize the direction
        step_x = dx / distance
        step_y = dy / distance

        # Check each point along the line of sight
        x, y = enemy_center
        for _ in range(int(distance)):
            x += step_x
            y += step_y

            # Convert world coordinates to chunk and tile coordinates
            chunk_x = math.floor(x / TILE_SIZE / CHUNK_SIZE)
            chunk_y = math.floor(y / TILE_SIZE / CHUNK_SIZE)
            tile_x = math.floor((x % (TILE_SIZE * CHUNK_SIZE)) / TILE_SIZE)
            tile_y = math.floor((y % (TILE_SIZE * CHUNK_SIZE)) / TILE_SIZE)

            # Check if the chunk exists
            if (chunk_x, chunk_y) not in chunks:
                return False  # Chunk doesn't exist, assume wall

            # Check if the tile is a wall
            if chunks[(chunk_x, chunk_y)][tile_y][tile_x] == 'WALL':
                return False  # Wall blocks line of sight

        return True 


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
