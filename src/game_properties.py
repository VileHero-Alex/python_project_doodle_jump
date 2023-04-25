import pygame


class GameProperties():
    def __init__(self):
        self.delta = 0
        self.record_height = 0
        self.size = 350, 550
        self.width, self.height = self.size
        self.FPS = 200
        self.screen = pygame.display.set_mode(self.size)
        self.screen.fill(pygame.Color('white'))
        self.clock = pygame.time.Clock()
