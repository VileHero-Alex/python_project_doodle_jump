import pygame
import random
from src.load_image import load_image


class Monster(pygame.sprite.Sprite):
    image = load_image("images/monster.png", 100, 100, (255, 255, 255))

    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = Monster.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y
        self.ax = self.rect.x
        self.vx = 1

    def update(self, *game_properties):
        self.rect.x += self.vx
        if self.rect.x >= self.ax + 3:
            self.vx = -1
        elif self.rect.x <= self.ax - 3:
            self.vx = 1
        if self.rect.y > game_properties[0].height:
            self.rect.x = random.randint(75, 275)
            self.ax = self.rect.x
            self.rect.y = -3160
        else:
            self.rect.y += game_properties[0].c

    def get_rect(self):
        return pygame.Rect(self.rect.x + 3, self.rect.y, 60, 60)
