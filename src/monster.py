import pygame
import random
import time
import math
from src.load_image import load_image


class Monster(pygame.sprite.Sprite):
    def __init__(self, y, game_properties, all_sprites, monsters):
        super().__init__(all_sprites, monsters)
        self.game_properties = game_properties
        self.image = load_image("images/monster.png",
                                100, 100, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.x, self.y = random.randint(50, game_properties.width - 150), y
        self.rect.x, self.rect.y = int(self.x), int(self.x)

    def offset(self):
        A = 13
        w = 7
        self.rect.x = int(self.x + A * math.cos(w * time.time()))

    def update(self, **kwargs):
        if self.y > self.game_properties.height:
            self.x = random.randint(75, 275)
            self.y = -3160
        else:
            self.y += self.game_properties.delta
        self.rect.y = int(self.y)
        self.offset()
