import pygame
from config.colors import *
from config.settings import *
from objects.grid import Grid
from objects.player import Player
from managers.music_manager import MusicManager


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.run = True
        self.clock = pygame.time.Clock()

        self.music_manager = MusicManager('./assets/endlessdungeon.mp3', 100)
        self.music_manager.play(5000)

        self.enemies = []

        self.grid = Grid(TILE_SIZE, CHUNK_SIZE)
        self.player = Player()
        self.camera_x_offset, self.camera_y_offset = 0, 0
        self.viewport_width, self.viewport_height = SCREEN_WIDTH // TILE_SIZE, SCREEN_HEIGHT // TILE_SIZE

    def loop(self):
        while self.run:
            self.run = self.handle_events()

            if self.run:
                self.update()
                self.draw()
                self.music_manager.fade_update()
                self.clock.tick(FPS)
                
        return 1 # MENU

    def draw(self):
        # CLEAR SCREEN
        self.screen.fill(BACKGROUND_COLOR)

        # GRID
        self.grid.draw(self.screen, int(self.camera_x_offset), int(self.camera_y_offset), self.viewport_width, self.viewport_height)
        self.player.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera_x_offset, self.camera_y_offset)

        # UPDATE
        pygame.display.update()

    def update(self):

        for enemy in self.enemies:
            enemy.update(self.player.world_x, self.player.world_y)

        self.player.update(self.camera_x_offset, self.camera_y_offset)

    def handle_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                
                if event.type == pygame.MOUSEWHEEL:
                    if event.y < 0:
                        self.player.change_selected_inventory_slot(1)
                    elif event.y > 0:
                        self.player.change_selected_inventory_slot(-1)
                
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.camera_y_offset -= PLAYER_SPEED
        if keys[pygame.K_s]:
            self.camera_y_offset += PLAYER_SPEED
        if keys[pygame.K_a]:
            self.camera_x_offset -= PLAYER_SPEED
        if keys[pygame.K_d]:
            self.camera_x_offset += PLAYER_SPEED


        return True