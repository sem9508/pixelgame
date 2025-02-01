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
        self.width = TILE_SIZE - ENEMY_TILE_OFFSET * 2
        self.height = TILE_SIZE - ENEMY_TILE_OFFSET * 2
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
    
    def check_collision(self, new_x, new_y, chunks):
        # Create a temporary Rect for the new position
        new_rect = pygame.Rect(new_x, new_y, self.width, self.height)

        # Calculate the range of tiles that the enemy occupies
        start_chunk_x = math.floor(new_x / TILE_SIZE / CHUNK_SIZE)
        start_chunk_y = math.floor(new_y / TILE_SIZE / CHUNK_SIZE)
        end_chunk_x = math.floor((new_x + self.width - 1) / TILE_SIZE / CHUNK_SIZE)
        end_chunk_y = math.floor((new_y + self.height - 1) / TILE_SIZE / CHUNK_SIZE)

        # Iterate over all chunks that the enemy occupies
        for chunk_x in range(start_chunk_x, end_chunk_x + 1):
            for chunk_y in range(start_chunk_y, end_chunk_y + 1):

                # Check if the chunk exists
                if (chunk_x, chunk_y) not in chunks:
                    return True  # Assume collision if chunk doesn't exist

                # Get the chunk data
                chunk = chunks[(chunk_x, chunk_y)]

                # Calculate the range of tiles that the enemy occupies within this chunk
                start_tile_x = max(0, math.floor((new_x % (TILE_SIZE * CHUNK_SIZE)) / TILE_SIZE))
                start_tile_y = max(0, math.floor((new_y % (TILE_SIZE * CHUNK_SIZE)) / TILE_SIZE))
                end_tile_x = min(CHUNK_SIZE - 1, math.floor((new_x + self.width - 1) % (TILE_SIZE * CHUNK_SIZE) / TILE_SIZE))
                end_tile_y = min(CHUNK_SIZE - 1, math.floor((new_y + self.height - 1) % (TILE_SIZE * CHUNK_SIZE) / TILE_SIZE))

                # Check all tiles within the bounding box
                for tile_y in range(start_tile_y, end_tile_y + 1):
                    for tile_x in range(start_tile_x, end_tile_x + 1):
                        if chunk[tile_y][tile_x] == 'WALL':
                            return True  # Collision with wall
        
        return False  # No collision


    def follow_player(self, player_x, player_y, chunks):
        # Calculate the direction to the player
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.hypot(dx, dy)

        if distance == 0:
            return  # Player and enemy are at the same position

        # Normalize the direction
        dx /= distance
        dy /= distance

        # Calculate potential new position
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed

        # Check for collisions in X and Y separately
        if not self.check_collision(new_x, self.y, chunks):
            self.x = new_x  # Update X position if no collision
        if not self.check_collision(self.x, new_y, chunks):
            self.y = new_y  # Update Y position if no collision

    def draw(self, screen, camera_x_offset, camera_y_offset):
        adjusted_x = self.x - camera_x_offset
        adjusted_y = self.y - camera_y_offset
        if (adjusted_x + self.width > 0 and adjusted_x < SCREEN_WIDTH and 
            adjusted_y + self.height > 0 and adjusted_y < SCREEN_HEIGHT):
            screen.blit(self.img, (adjusted_x, adjusted_y))

    def update(self):

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)