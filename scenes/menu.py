import pygame
from config.settings import *

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.run = True
        self.clock = pygame.time.Clock()

    def loop(self):
        while self.run:
            self.run = self.handle_events()
            
            if self.run:
                self.update()
                self.draw()
                self.clock.tick(FPS)

            break # NO MENU NOW
        return -1
    
    def draw(self):
        self.screen.fill(MENU_COLOR)

        pygame.display.update()

    def update(self):
        pass
         
    
    def handle_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                
        return True