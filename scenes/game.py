import pygame
from config.colors import *
from config.settings import *
from objects.grid import Grid
from objects.player import Player
from managers.music_manager import MusicManager
from managers.enemy_manager import EnemyManager
import math
from objects.camera import Camera

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.run = True
        self.clock = pygame.time.Clock()

        self.music_manager = MusicManager('./assets/endlessdungeon.mp3', 100)
        self.music_manager.play(5000)

        self.enemy_manager = EnemyManager()
        self.camera = Camera(0, 0)

        self.grid = Grid(TILE_SIZE, CHUNK_SIZE)
        self.player = Player()
        self.viewport_width, self.viewport_height = SCREEN_WIDTH // TILE_SIZE, SCREEN_HEIGHT // TILE_SIZE

    def loop(self):
        while self.run:
            self.run = self.handle_events()

            if self.run:
                self.update()
                self.draw()
                self.clock.tick(FPS)
                pygame.display.set_caption(str(math.floor(self.clock.get_fps())))
        return 1 # MENU

    def draw(self):
        # CLEAR SCREEN
        self.screen.fill(BACKGROUND_COLOR)

        # GRID
        self.grid.draw(self.screen, self.camera, self.viewport_width, self.viewport_height, self.enemy_manager, self.player.world_x+self.player.width//2, self.player.world_y+self.player.height//2)
        self.enemy_manager.draw(self.screen, self.camera)
        self.grid.second_draw(self.screen)
        self.player.draw(self.screen)


        # UPDATE
        pygame.display.update()

    def update(self):
        self.music_manager.fade_update()
        self.player.update()
        self.enemy_manager.update(self.player.rect, self.camera, self.grid.chunks)
        self.camera.update(self.player.rect)

    def handle_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                
                if event.type == pygame.MOUSEWHEEL:
                    if event.y < 0:
                        self.player.change_selected_inventory_slot(1)
                    elif event.y > 0:
                        self.player.change_selected_inventory_slot(-1)
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.player.attacking == False:
                        self.player.start_attack()
            
        keys = pygame.key.get_pressed()

        dir_x, dir_y = 0, 0
        if keys[pygame.K_w]:
            dir_y -= 1
        if keys[pygame.K_s]:
            dir_y += 1
        if keys[pygame.K_a]:
            dir_x -= 1
        if keys[pygame.K_d]:
            dir_x += 1
            
        self.player.move(dir_x, dir_y, self.grid)

        return True
