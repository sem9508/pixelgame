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
        self.chunks = {(0, 0): [['FLOOR' for _ in range(CHUNK_SIZE)] for _ in range(CHUNK_SIZE)]}
        self.wall_rects = []  # List to store Rect objects for walls
        self.loot_tiles = []

    def generate_chunk(self, chunk_x, chunk_y):
        chunk = []
        for y in range(self.chunk_size):
            row = []
            for x in range(self.chunk_size):
                world_x = (chunk_x * self.chunk_size + x) / NOISE_SCALE
                world_y = (chunk_y * self.chunk_size + y) / NOISE_SCALE

                noise_value = noise.pnoise2(world_x, world_y, octaves=NOISE_OCTAVES, persistence=NOSIE_PERSISTENCE, lacunarity=NOISE_LACUNARITY, base=SEED)

                tile_type = self.map_noise_to_tile(noise_value)
                if tile_type == 'LOOT':
                    self.loot_tiles.append((
                        (chunk_x * CHUNK_SIZE + x) * TILE_SIZE,  # Converteer naar pixelcoördinaten
                        (chunk_y * CHUNK_SIZE + y) * TILE_SIZE   # Converteer naar pixelcoördinaten
                    ))
                    tile_type = 'FLOOR'
                row.append(tile_type)

                # If the tile is a wall, add its Rect to the list
                if tile_type == 'WALL':
                    rect = pygame.Rect(
                        (chunk_x * CHUNK_SIZE + x) * TILE_SIZE,
                        (chunk_y * CHUNK_SIZE + y) * TILE_SIZE,
                        TILE_SIZE,
                        TILE_SIZE
                    )
                    self.wall_rects.append(rect)
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
            return True
        
        step_x = x_diff / distance
        step_y = y_diff / distance

        x, y = start_x, start_y
        for _ in range(int(distance)):
            x += step_x
            y += step_y
            
            chunk_x, tile_x = divmod(int(x), CHUNK_SIZE)
            chunk_y, tile_y = divmod(int(y), CHUNK_SIZE)

            chunk = grid.get_chunk(chunk_x, chunk_y, enemy_manager)
            tile = chunk[tile_y][tile_x]

            if tile == 'WALL':
                return False

        return True
    
    def update_chunk(self, chunk_x, chunk_y, chunk):
        self.chunks[(chunk_x, chunk_y)] = chunk
        return chunk
        
    def draw(self, screen, camera, viewport_width, viewport_height, enemy_manager, player_x, player_y):
        self.to_draw = []
        start_chunk_x = int(camera.x // (self.chunk_size * self.tile_size) - 1)
        start_chunk_y = int(camera.y // (self.chunk_size * self.tile_size) - 1)
        end_chunk_x = int((camera.x + viewport_width * self.tile_size) // (self.chunk_size * self.tile_size) + 1)
        end_chunk_y = int((camera.y + viewport_height * self.tile_size) // (self.chunk_size * self.tile_size) + 1)

        for chunk_y in range(start_chunk_y, end_chunk_y + 1):
            for chunk_x in range(start_chunk_x, end_chunk_x + 1):
                chunk = self.get_chunk(chunk_x, chunk_y, enemy_manager)
                for row in range(self.chunk_size):
                    for col in range(self.chunk_size):
                        world_x = (chunk_x * self.chunk_size + col) * self.tile_size
                        world_y = (chunk_y * self.chunk_size + row) * self.tile_size

                        distance = math.sqrt((player_x - world_x)**2 + (player_y - world_y)**2) / self.tile_size

                        if not (distance <= VISION_RADIUS and self.is_tile_visible(player_x // self.tile_size, player_y // self.tile_size, world_x // self.tile_size, world_y // self.tile_size, enemy_manager)) and LIMITED_VISION:
                            self.to_draw.append([world_x, world_y, camera])

                        
                        else:
                            tile = chunk[row][col]
                            pygame.draw.rect(screen, self.get_tile_color(tile), (world_x - camera.x, world_y - camera.y, self.tile_size, self.tile_size))


                    if SHOW_CHUNK_BORDERS:
                        chunk_start_x = chunk_x * CHUNK_SIZE * TILE_SIZE - camera.x
                        chunk_start_y = chunk_y * CHUNK_SIZE * TILE_SIZE - camera.y
                        chunk_end_x = (chunk_x + 1) * CHUNK_SIZE * TILE_SIZE - camera.x
                        chunk_end_y = (chunk_y + 1) * CHUNK_SIZE * TILE_SIZE - camera.y

                        pygame.draw.line(screen, RED, (chunk_start_x, chunk_start_y), (chunk_end_x, chunk_start_y))
                        pygame.draw.line(screen, RED, (chunk_start_x, chunk_start_y), (chunk_start_x, chunk_end_y))
                        pygame.draw.line(screen, RED, (chunk_start_x, chunk_end_y), (chunk_end_x, chunk_end_y))
                        pygame.draw.line(screen, RED, (chunk_end_x, chunk_start_y), (chunk_end_x, chunk_end_y))

                self.chunks[(chunk_x, chunk_y)] = self.update_chunk(chunk_x, chunk_y, chunk)

        for loot_tile in self.loot_tiles:
            pygame.draw.rect(
                screen,
                CYAN,
                (
                    loot_tile[0] - camera.x,  # Correcte X-coördinaat
                    loot_tile[1] - camera.y,  # Correcte Y-coördinaat
                    TILE_SIZE,
                    TILE_SIZE
                )
            )

    def second_draw(self, screen):
        for item in self.to_draw:
            world_x = item[0]
            world_y = item[1]
            camera = item[2]
            pygame.draw.rect(screen, self.get_tile_color('WALL'), (world_x - camera.x, world_y - camera.y, self.tile_size, self.tile_size))