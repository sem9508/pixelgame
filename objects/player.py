import pygame
from config.colors import *
from config.settings import *
import math
from objects.weapon import Weapon

class Player:
    def __init__(self):
        # Player attributes
        self.width = TILE_SIZE - PLAYER_TILE_OFFSET * 2
        self.height = TILE_SIZE - PLAYER_TILE_OFFSET * 2
        self.draw_x = SCREEN_WIDTH // 2 - self.width // 2
        self.draw_y = SCREEN_HEIGHT // 2 - self.height // 2
        self.world_x = self.draw_x
        self.world_y = self.draw_y
        self.rect = pygame.Rect(self.world_x, self.world_y, self.width, self.height)
        self.speed = PLAYER_SPEED
        
        # Inventory
        self.inventory = []
        self.inventory_height = 100
        self.max_inventory = 8
        self.inventory_selected_slot = 0

        # Load player image
        self.img = pygame.image.load('./assets/player.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, (self.width, self.height))

        # Weapons
        self.attacking = False
        self.attack_cooldown = 0
        self.current_weapon = None
        self.initialize_weapons()
        self.current_weapon = self.inventory[0]

    def initialize_weapons(self):
        sword = Weapon("Sword", damage=10, attack_range=50, cooldown=30, attack_duration=10, weapon_type='melee')
        bow = Weapon("Bow", damage=5, attack_range=150, cooldown=40, attack_duration=15, weapon_type='ranged')
        self.inventory = [sword, bow]
        
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

    def start_attack(self):
        if not self.attacking and self.attack_cooldown <= 0 and self.current_weapon:
            self.attacking = True
            self.attack_cooldown = self.current_weapon.cooldown

    def update(self):
        if self.attacking:
            self.current_weapon.attack_duration -= 1
            if self.current_weapon.attack_duration <= 0:
                self.attacking = False
                self.current_weapon.attack_duration = 10  # Reset based on weapon
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def draw(self, screen):
        screen.blit(self.img, (self.draw_x, self.draw_y, self.width, self.height))
        self.draw_inventory(screen)

        if self.attacking:
            pygame.draw.rect(screen, RED, self.get_melee_attack_rect_draw())

    def draw_inventory(self, screen):
        inventory_width = SCREEN_WIDTH - (2 * SCREEN_WIDTH / self.max_inventory)
        pygame.draw.rect(screen, (80, 80, 80), (SCREEN_WIDTH/self.max_inventory, SCREEN_HEIGHT - self.inventory_height - 75, inventory_width, self.inventory_height))
        slot_width = inventory_width / self.max_inventory

        pygame.draw.rect(screen, (100, 100, 100), (SCREEN_WIDTH / self.max_inventory + self.inventory_selected_slot * slot_width, SCREEN_HEIGHT - self.inventory_height - 75, slot_width, self.inventory_height))


        for i in range(1, self.max_inventory):
            x = SCREEN_WIDTH / self.max_inventory + i * slot_width
            pygame.draw.line(screen, (40, 40, 40), (x, SCREEN_HEIGHT - self.inventory_height - 75), (x, SCREEN_HEIGHT - 75))

    def get_melee_attack_rect_world(self):
            # Adjust attack based on the weapon
        attack_rect = pygame.Rect(
            self.world_x + self.width,  # Attack to the right of the player
            self.world_y + self.height // 4,
            self.current_weapon.attack_range,
            self.height // 2
        )
        return attack_rect
    
    def get_melee_attack_rect_draw(self):
            # Adjust attack based on the weapon
        attack_rect = pygame.Rect(
            self.draw_x + self.width,  # Attack to the right of the player
            self.draw_y + self.height // 4,
            self.current_weapon.attack_range,
            self.height // 2
        )
        return attack_rect
        
    def check_attack_collision(self, enemies):
        if self.attacking and self.current_weapon.type == 'melee':
            attack_rect = self.get_melee_attack_rect_world()
            for enemy in enemies:
                if attack_rect.colliderect(enemy.rect):
                    enemy.take_damage(self.current_weapon.damage)

    def change_selected_inventory_slot(self, dir):
        if dir < 0:
            self.inventory_selected_slot -= 1
            if self.inventory_selected_slot < 0:
                self.inventory_selected_slot = self.max_inventory
        
        elif dir > 0:
            self.inventory_selected_slot += 1
            if self.inventory_selected_slot > self.max_inventory-1:
                self.inventory_selected_slot = 0
