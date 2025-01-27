import pygame
import random
import noise
from config.colors import *
from objects.enemy import Enemy
from config.settings import *

class Grid:
    def __init__(self, tile_size, chunk_size):
        self.tile_size = tile_size
        self.chunk_size = chunk_size
        self.enemies = []
        self.spawned_enemies = set()
        self.chunks = {(0, 0):[['FLOOR' for _ in range(CHUNK_SIZE)] for _ in range(CHUNK_SIZE)]}

    def generate_chunk(self, chunk_x, chunk_y):
        chunk = []
        for y in range(self.chunk_size):
            row = []
            for x in range(self.chunk_size):
                world_x = (chunk_x * self.chunk_size + x) / NOISE_SCALE
                world_y = (chunk_y * self.chunk_size + y) / NOISE_SCALE

                noise_value = noise.pnoise2(world_x, world_y, octaves=NOISE_OCTAVES, persistence=NOSIE_PERSISTENCE, lacunarity=NOISE_LACUNARITY, base=SEED)

                tile_type = self.map_noise_to_tile(noise_value)
                row.append(tile_type)
            chunk.append(row)

        return chunk
    
    def map_noise_to_tile(self, noise_value):
        if noise_value < -0.4:
            return 'LOOT'
        elif noise_value < -0.3:
            return 'ENEMY'
        elif noise_value < 0.05:
            return 'FLOOR'
        elif noise_value < 0.4:
            return 'WALL'
        else:
            return 'WALL'
    
    def get_tile_color(self, tile_type):
        if tile_type == 'LOOT':
            return (0, 255, 255)
        elif tile_type == 'FLOOR':
            return (50, 50, 50)
        elif tile_type == 'WALL':
            return (10, 10, 10)
        elif tile_type == 'MOUNTAIN':
            return (139, 137, 137)
        else:
            return (0, 0, 0)
        
    def spawn_enemy(self, chunk_x, chunk_y, row, col):
        world_x = (chunk_x * self.chunk_size + col) * self.tile_size
        world_y = (chunk_y * self.chunk_size + row) * self.tile_size

        self.enemies.append(Enemy(world_x, world_y, 3))

    def update_tile(self, chunk, row, col, chunk_x, chunk_y):
        tile_type = chunk[row][col]
        if tile_type == 'ENEMY':
            # Check if this tile has already spawned an enemy
            if (chunk_x, chunk_y, row, col) not in self.spawned_enemies:
                # Spawn the enemy and mark the tile as processed
                self.spawn_enemy(chunk_x, chunk_y, row, col)
                self.spawned_enemies.add((chunk_x, chunk_y, row, col))
            # Change the tile to 'FLOOR' after spawning the enemy
            chunk[row][col] = 'FLOOR'
        return tile_type, chunk

    def get_chunk(self, chunk_x, chunk_y):
        if (chunk_x, chunk_y) not in self.chunks:
            self.chunks[(chunk_x, chunk_y)] = self.generate_chunk(chunk_x, chunk_y)
        return self.chunks[(chunk_x, chunk_y)]
    
    def update_chunk(self, chunk_x, chunk_y, chunk):
        self.chunks[(chunk_x, chunk_y)] = chunk
        return chunk
    
    def draw(self, screen, camera_x_offset, camera_y_offset, viewport_width, viewport_height):
        start_chunk_x = camera_x_offset // (self.chunk_size * self.tile_size) - 1
        start_chunk_y = camera_y_offset // (self.chunk_size * self.tile_size) - 1
        end_chunk_x = (camera_x_offset + viewport_width * self.tile_size) // (self.chunk_size * self.tile_size) + 1
        end_chunk_y = (camera_y_offset + viewport_height * self.tile_size) // (self.chunk_size * self.tile_size) + 1

        for chunk_y in range(start_chunk_y, end_chunk_y + 1):
            for chunk_x in range(start_chunk_x, end_chunk_x + 1):
                chunk = self.get_chunk(chunk_x, chunk_y)

                for row in range(self.chunk_size):
                    for col in range(self.chunk_size):
                        world_x = (chunk_x * self.chunk_size + col) * self.tile_size
                        world_y = (chunk_y * self.chunk_size + row) * self.tile_size

                        chunk[row][col], chunk = self.update_tile(chunk, row, col, chunk_x, chunk_y)
                        tile = chunk[row][col]
                        pygame.draw.rect(screen, self.get_tile_color(tile), (world_x - camera_x_offset, world_y - camera_y_offset, self.tile_size, self.tile_size))

                if SHOW_CHUNK_BORDERS:
                    chunk_start_x = chunk_x * CHUNK_SIZE * TILE_SIZE - camera_x_offset
                    chunk_start_y = chunk_y * CHUNK_SIZE * TILE_SIZE - camera_y_offset
                    chunk_end_x = (chunk_x + 1) * CHUNK_SIZE * TILE_SIZE - camera_x_offset
                    chunk_end_y = (chunk_y + 1) * CHUNK_SIZE * TILE_SIZE - camera_y_offset

                    pygame.draw.line(screen, RED, (chunk_start_x, chunk_start_y), (chunk_end_x, chunk_start_y))
                    pygame.draw.line(screen, RED, (chunk_start_x, chunk_start_y), (chunk_start_x, chunk_end_y))
                    pygame.draw.line(screen, RED, (chunk_start_x, chunk_end_y), (chunk_end_x, chunk_end_y))
                    pygame.draw.line(screen, RED, (chunk_end_x, chunk_start_y), (chunk_end_x, chunk_end_y))

                self.chunks[(chunk_x, chunk_y)] = self.update_chunk(chunk_x, chunk_y, chunk)
        
        return self.enemies
