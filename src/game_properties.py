import pygame


class GameProperties():
    def __init__(self):
        self.max_y = 0
        self.size = 350, 550
        self.width, self.height = self.size
        self.h = 0
        self.c = 0
        self.screen = pygame.display.set_mode(self.size)
        self.screen.fill(pygame.Color('white'))
        self.FPS = 50
        self.left = 0
        self.clock = pygame.time.Clock()
