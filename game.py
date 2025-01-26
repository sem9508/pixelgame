import pygame
from constants import *
import sys
from grid import Grid

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.run = True
        self.clock = pygame.time.Clock()

        self.grid = Grid(TILE_SIZE, CHUNK_SIZE)

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
            self.camera_y_offset -= PLAYER_SPEED
        if keys[pygame.K_s]:
            self.camera_y_offset += PLAYER_SPEED
        if keys[pygame.K_a]:
            self.camera_x_offset -= PLAYER_SPEED
        if keys[pygame.K_d]:
            self.camera_x_offset += PLAYER_SPEED

        return True