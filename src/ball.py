import pygame
import math
import time
import random


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, game_properties, *args):
        super().__init__(*args)
        self.game_properties = game_properties
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA, 32)
        pygame.draw.ellipse(self.image, pygame.Color("red"), (0, 0, 20, 20))
        self.rect = pygame.Rect(x, y, 20, 20)
        self.x0 = self.x = x
        self.y0 = self.y = y
        self.param = random.random() * 2 * math.pi
        self.rect.x, self.rect.y = int(x), int(y)

        self.vy = 700
        self.t0 = time.time()

    def offset(self):
        A = 10
        w = 40
        self.rect.x = int(self.x0 + A * math.cos(w * time.time() + self.param))

    def update(self):
        self.y += self.game_properties.delta
        self.y0 += self.game_properties.delta
        self.y = self.y0 - self.vy * (time.time() - self.t0)
        self.rect.y = int(self.y)
        self.offset()

        if self.y < -20:
            self.kill()
