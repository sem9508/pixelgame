import pygame
from config.colors import *
from config.settings import *
import sys
from objects.grid import Grid
from objects.player import Player

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.run = True
        self.clock = pygame.time.Clock()

        self.grid = Grid(TILE_SIZE, CHUNK_SIZE)
        self.player = Player(0, 0)

        self.camera_x_offset, self.camera_y_offset = 0, 0
        self.viewport_width, self.viewport_height = SCREEN_WIDTH // TILE_SIZE, SCREEN_HEIGHT // TILE_SIZE

    def loop(self):
        while self.run:
            self.run = self.handle_events()

            if self.run:
                self.update()
                self.draw()
                self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

    def draw(self):
        # CLEAR SCREEN
        self.screen.fill(BACKGROUND_COLOR)

        # GRID
        self.grid.draw(self.screen, self.camera_x_offset, self.camera_y_offset, self.viewport_width, self.viewport_height)
        self.player.draw(self.screen)

        # UPDATE
        pygame.display.update()

    def update(self):
        pass

    def handle_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move_y(-1)
        if keys[pygame.K_s]:
            self.player.move_y(1)
        if keys[pygame.K_a]:
            self.player.move_x(-1)
        if keys[pygame.K_d]:
            self.player.move_x(1)


        return True