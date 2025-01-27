import pygame
import random
import noise
from config.colors import *
from config.settings import *

class Grid:
    def __init__(self, tile_size, chunk_size):
        self.tile_size = tile_size
        self.chunk_size = chunk_size

        self.chunks = {}

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
        if tile_type == 'ENEMY':
            return (255, 0, 0)
        elif tile_type == 'FLOOR':
            return (50, 50, 50)
        elif tile_type == 'WALL':
            return (10, 10, 10)
        elif tile_type == 'MOUNTAIN':
            return (139, 137, 137)
        else:
            return (0, 0, 0)

    def get_chunk(self, chunk_x, chunk_y):
        if (chunk_x, chunk_y) not in self.chunks:
            self.chunks[(chunk_x, chunk_y)] = self.generate_chunk(chunk_x, chunk_y)
        return self.chunks[(chunk_x, chunk_y)]
    
    def draw(self, screen, camera_x_offset, camera_y_offset, viewport_width, viewport_height):
        start_chunk_x = camera_x_offset // (self.chunk_size*self.tile_size) - 1
        start_chunk_y = camera_y_offset // (self.chunk_size*self.tile_size) - 1
        end_chunk_x = (camera_x_offset + viewport_width * self.tile_size) // (self.chunk_size * self.tile_size)
        end_chunk_y = (camera_y_offset + viewport_height * self.tile_size) // (self.chunk_size * self.tile_size)


        for chunk_y in range(start_chunk_y, end_chunk_y + 1):
            for chunk_x in range(start_chunk_x, end_chunk_x + 1):
                chunk = self.get_chunk(chunk_x, chunk_y)

                for row in range(self.chunk_size):
                    for col in range(self.chunk_size):
                        world_x = (chunk_x * self.chunk_size + col) * self.tile_size
                        world_y = (chunk_y * self.chunk_size + row) * self.tile_size

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

                        

                    