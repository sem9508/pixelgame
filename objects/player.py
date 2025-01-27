import pygame
from config.colors import *
from config.settings import *

class Player:
    def __init__(self):
        self.width = TILE_SIZE - PLAYER_TILE_OFFSET*2
        self.height = TILE_SIZE - PLAYER_TILE_OFFSET*2
        self.x = SCREEN_WIDTH // 2 - self.width // 2  # This is the screen-centered position
        self.y = SCREEN_HEIGHT // 2 - self.height // 2

        self.world_x = self.x  # Track player world position
        self.world_y = self.y
        self.img = pygame.image.load('./assets/player.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, (self.width, self.height))

        self.speed = PLAYER_SPEED

    def update(self, camera_x_offset, camera_y_offset):
        # Update player's world position based on the camera offset
        self.world_x = self.x + camera_x_offset
        self.world_y = self.y + camera_y_offset

    def draw(self, screen):
        screen.blit(self.img, (self.x + PLAYER_TILE_OFFSET, self.y + PLAYER_TILE_OFFSET, self.width, self.height))
