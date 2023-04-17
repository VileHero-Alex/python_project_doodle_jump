import pygame
from src.load_image import load_image


class GameOver(pygame.sprite.Sprite):

    def __init__(self, group, game_properties):
        super().__init__(group)
        self.image = load_image(
            "images/GameOver.jpg", *game_properties.size)
        self.rect = self.image.get_rect()
        self.rect.x = -600
        self.rect.y = 0

    def update(self, *game_properties):
        if self.rect.x < 0:
            self.rect.x += 1
