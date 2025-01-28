import pygame
import random
import noise
from config.colors import *
from objects.enemy import Enemy
from config.settings import *
import math

class Grid:
    def __init__(self, tile_size, chunk_size):
        self.tile_size = tile_size
        self.chunk_size = chunk_size
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
        if noise_value < -0.37:
            return 'LOOT'
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

    def update_tile(self, chunk, row, col, chunk_x, chunk_y):
        pass

    def get_chunk(self, chunk_x, chunk_y, enemy_manager):
        if (chunk_x, chunk_y) not in self.chunks:
            self.chunks[(chunk_x, chunk_y)] = self.generate_chunk(chunk_x, chunk_y)
            enemy_manager.spawn_enemy_new_chunk(chunk_x, chunk_y, self.chunks)

        return self.chunks[(chunk_x, chunk_y)]
    
    def is_tile_visible(grid, start_x, start_y, end_x, end_y, enemy_manager):
        x_diff = end_x - start_x
        y_diff = end_y - start_y
        distance = math.sqrt(x_diff**2 + y_diff**2)
        
        if distance == 0:
            return True  # We're standing on the same tile
        
        step_x = x_diff / distance
        step_y = y_diff / distance

        x, y = start_x, start_y
        for _ in range(int(distance)):
            # Step along the ray, check if we hit a wall
            x += step_x
            y += step_y
            
            chunk_x, tile_x = divmod(int(x), CHUNK_SIZE)
            chunk_y, tile_y = divmod(int(y), CHUNK_SIZE)
            
            # Get the chunk and tile
            chunk = grid.get_chunk(chunk_x, chunk_y, enemy_manager)
            tile = chunk[tile_y][tile_x]

            if tile == 'WALL':  # Block the ray if it's a wall
                return False

        return True
    
    def update_chunk(self, chunk_x, chunk_y, chunk):
        self.chunks[(chunk_x, chunk_y)] = chunk
        return chunk
        
    def draw(self, screen, camera_x_offset, camera_y_offset, viewport_width, viewport_height, enemy_manager, player_x, player_y):
        start_chunk_x = camera_x_offset // (self.chunk_size * self.tile_size) - 1
        start_chunk_y = camera_y_offset // (self.chunk_size * self.tile_size) - 1
        end_chunk_x = (camera_x_offset + viewport_width * self.tile_size) // (self.chunk_size * self.tile_size) + 1
        end_chunk_y = (camera_y_offset + viewport_height * self.tile_size) // (self.chunk_size * self.tile_size) + 1

        player_chunk_x = player_x // (self.chunk_size * self.tile_size)
        player_chunk_y = player_y // (self.chunk_size * self.tile_size)
        
        # Loop over all chunks
        for chunk_y in range(start_chunk_y, end_chunk_y + 1):
            for chunk_x in range(start_chunk_x, end_chunk_x + 1):
                chunk = self.get_chunk(chunk_x, chunk_y, enemy_manager)
                for row in range(self.chunk_size):
                    for col in range(self.chunk_size):
                        world_x = (chunk_x * self.chunk_size + col) * self.tile_size
                        world_y = (chunk_y * self.chunk_size + row) * self.tile_size

                        # Calculate tile's distance to the player
                        distance = math.sqrt((player_x - world_x)**2 + (player_y - world_y)**2) / self.tile_size

                        # Check if within vision radius and if there's line of sight
                        if not (distance <= VISION_RADIUS and self.is_tile_visible(player_x // self.tile_size, player_y // self.tile_size, world_x // self.tile_size, world_y // self.tile_size, enemy_manager)):
                            pygame.draw.rect(screen, self.get_tile_color('WALL'), (world_x - camera_x_offset, world_y - camera_y_offset, self.tile_size, self.tile_size))

                        
                        else:
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
