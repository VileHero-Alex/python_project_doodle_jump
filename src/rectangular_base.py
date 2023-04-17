import pygame


class RectangularBase(pygame.sprite.Sprite):

    def __init__(self, pl):
        super().__init__()
        self.rect = pl.get_rect()
