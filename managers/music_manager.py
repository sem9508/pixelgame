import pygame

class MusicManager:
    def __init__(self, song, fade_duration):
        pygame.mixer.init()
        pygame.mixer.music.load(song)
        self.volume = 0
        self.set_volume(self.volume)

        self.timer = 0
        self.fade_duration = fade_duration

    def play(self, fade_in_time):
        pygame.mixer.music.play(-1, 0, fade_in_time)
    
    def pause(self):
        pygame.mixer.music.pause()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def fade_update(self):
        if self.timer < self.fade_duration:
            self.volume += 1/self.fade_duration
            self.timer += 1
            self.set_volume(self.volume)