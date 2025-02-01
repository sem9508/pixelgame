import pygame
from config.colors import *
from config.settings import *
import math

class Player:
    def __init__(self):
        self.width = TILE_SIZE - PLAYER_TILE_OFFSET*2
        self.height = TILE_SIZE - PLAYER_TILE_OFFSET*2

        self.draw_x = SCREEN_WIDTH // 2 - self.width // 2
        self.draw_y = SCREEN_HEIGHT // 2 - self.height // 2
        self.world_x = self.draw_x  # Track player world position
        self.world_y = self.draw_y

        self.inventory = []
        self.max_inventory = 8
        self.inventory_height = 100
        self.inventory_selected_slot = 0
        self.img = pygame.image.load('./assets/player.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, (self.width, self.height))

        self.rect = pygame.Rect(self.world_x, self.world_y, self.width, self.height)

        self.speed = PLAYER_SPEED
        
    def move(self, dir_x, dir_y, grid):
        new_x = self.world_x + dir_x * PLAYER_SPEED
        new_y = self.world_y + dir_y * PLAYER_SPEED

        new_rect_x = pygame.Rect(new_x, self.world_y, self.width, self.height)
        new_rect_y = pygame.Rect(self.world_x, new_y, self.width, self.height)

        collision_x = False
        for wall_rect in grid.wall_rects:
            if new_rect_x.colliderect(wall_rect):
                collision_x = True
                break

        collision_y = False
        for wall_rect in grid.wall_rects:
            if new_rect_y.colliderect(wall_rect):
                collision_y = True
                break

        if not collision_x:
            self.world_x = new_x
        if not collision_y:
            self.world_y = new_y

        self.rect.topleft = (self.world_x, self.world_y)

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.img, (self.draw_x, self.draw_y, self.width, self.height))
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
