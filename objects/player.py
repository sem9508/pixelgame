import pygame
from config.colors import *
from config.settings import *

class Player:
    def __init__(self):
        self.width = TILE_SIZE - PLAYER_TILE_OFFSET*2
        self.height = TILE_SIZE - PLAYER_TILE_OFFSET*2
        self.x = SCREEN_WIDTH // 2 - self.width // 2  # This is the screen-centered position
        self.y = SCREEN_HEIGHT // 2 - self.height // 2
        self.inventory = []
        self.max_inventory = 8
        self.world_x = self.x  # Track player world position
        self.world_y = self.y
        self.inventory_height = 100
        self.inventory_selected_slot = 0
        self.img = pygame.image.load('./assets/player.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, (self.width, self.height))

        self.speed = PLAYER_SPEED

    def update(self, camera_x_offset, camera_y_offset):
        # Update player's world position based on the camera offset
        self.world_x = self.x + camera_x_offset
        self.world_y = self.y + camera_y_offset

    def draw(self, screen):
        screen.blit(self.img, (self.x + PLAYER_TILE_OFFSET, self.y + PLAYER_TILE_OFFSET, self.width, self.height))
        self.draw_inventory(screen)

    def draw_inventory(self, screen):
        inventory_width = SCREEN_WIDTH - (2 * SCREEN_WIDTH / self.max_inventory)
        pygame.draw.rect(screen, (80, 80, 80), (SCREEN_WIDTH/self.max_inventory, SCREEN_HEIGHT - self.inventory_height - 75, inventory_width, self.inventory_height))
        slot_width = inventory_width / self.max_inventory

        pygame.draw.rect(screen, (100, 100, 100), (SCREEN_WIDTH / self.max_inventory + self.inventory_selected_slot * slot_width, SCREEN_HEIGHT - self.inventory_height - 75, slot_width, self.inventory_height))


        for i in range(1, self.max_inventory):
            x = SCREEN_WIDTH / self.max_inventory + i * slot_width
            pygame.draw.line(screen, (40, 40, 40), (x, SCREEN_HEIGHT - self.inventory_height - 75), (x, SCREEN_HEIGHT - 75))

    def change_selected_inventory_slot(self, dir):
        if dir < 0:
            self.inventory_selected_slot -= 1
            if self.inventory_selected_slot < 0:
                self.inventory_selected_slot = self.max_inventory
        
        elif dir > 0:
            self.inventory_selected_slot += 1
            if self.inventory_selected_slot > self.max_inventory-1:
                self.inventory_selected_slot = 0
