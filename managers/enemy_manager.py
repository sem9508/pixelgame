import pygame
import random
from config.settings import *
from objects.enemy import Enemy

class EnemyManager:
    def __init__(self):
        self.spawn_rate = ENEMY_SPAWN_RATE
        self.enemies = []

    def spawn_enemy(self, x, y):
        self.enemies.append(Enemy(x, y, random.randrange(MIN_ENEMY_SPEED, MAX_ENEMY_SPEED)))

    def spawn_enemy_new_chunk(self, chunk_x, chunk_y, chunks):
        # Get the chunk the player just entered
        if (chunk_x, chunk_y) in chunks:
            chunk = chunks[(chunk_x, chunk_y)]
            for _ in range(random.randint(MIN_ENEMIES_PER_CHUNK, MAX_ENEMIES_PER_CHUNK)):
                # Randomly choose a tile in the chunk to spawn an enemy
                spawn_row = random.randint(0, CHUNK_SIZE - 1)
                spawn_col = random.randint(0, CHUNK_SIZE - 1)
                
                # Make sure the enemy spawns on a walkable tile (e.g., 'FLOOR')
                if chunk[spawn_row][spawn_col] == 'FLOOR':
                    # Convert chunk coordinates to world coordinates
                    enemy_x = (chunk_x * CHUNK_SIZE + spawn_col) * TILE_SIZE
                    enemy_y = (chunk_y * CHUNK_SIZE + spawn_row) * TILE_SIZE

                    # Spawn the enemy at this position
                    self.spawn_enemy(enemy_x, enemy_y)

    def draw(self, screen, camera):
        for enemie in self.enemies:
            enemie.draw(screen, camera.x, camera.y)