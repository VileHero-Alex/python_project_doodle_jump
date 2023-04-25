import pygame
import random
import time
from src.load_image import load_image


class Platform(pygame.sprite.Sprite):
    v0y = 400

    def __init__(self, y, color, game_properties, *groups, **kwargs):
        super().__init__(*groups)
        self.game_properties = game_properties
        self.x, self.y = random.randint(5, self.game_properties.width - 50), y
        self.color = color
        self.image = pygame.Surface((50, 30), pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(self.x, self.y, 50, 1)
        pygame.draw.rect(self.image, pygame.Color(color), (0, 20, 50, 10))

    def update(self):
        if self.y <= self.game_properties.height:
            self.y += self.game_properties.delta
        else:
            self.x = random.randint(10, self.game_properties.width - 60)
            self.y = -50
        self.rect.x, self.rect.y = int(self.x), int(self.y)


class MovingPlatform(Platform):
    def __init__(self, y, color, *groups, **kwargs):
        super().__init__(y, color, *groups, **kwargs)
        self.vx = (random.randint(0, 1) * 2 - 1) * 50
        self.border = (5, self.game_properties.width - 55)
        self.last_change_time = time.time()
        self.x0 = self.x

    def update(self):
        delta_time = time.time() - self.last_change_time
        self.x = self.x0 + self.vx * delta_time
        if self.x <= self.border[0] and self.vx < 0 or \
            self.x >= self.border[1] and self.vx > 0:
            
            self.last_change_time = time.time()
            self.x0 = self.x
            self.vx = -self.vx
        super().update()


class BreakablePlatform(Platform):
    def __init__(self, y, color, *groups, **kwargs):
        self.time = -1
        super().__init__(y, color, *groups, **kwargs)

    def update(self):
        if self.time + 0.5 < time.time() and self.time != -1:
            self.destroyed()
        if self.y <= self.game_properties.height:
            self.y += self.game_properties.delta
        else:
            self.x = random.randint(10, self.game_properties.width - 60)
            self.y = -50
            pygame.draw.rect(self.image, pygame.Color("grey"), (0, 20, 50, 10))
        self.rect.x, self.rect.y = int(self.x), int(self.y)

    def broken(self):
        self.time = time.time()
        self.image = pygame.Surface((50, 30), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color("grey"), (0, 20, 15, 10))
        pygame.draw.rect(self.image, pygame.Color("grey"), (18, 20, 14, 10))
        pygame.draw.rect(self.image, pygame.Color("grey"), (35, 20, 15, 10))

    def destroyed(self):
        self.image = pygame.Surface((50, 30), pygame.SRCALPHA, 32)
        self.time = -1
        self.block = True


class Trampoline(Platform):
    v0y = 650

    def __init__(self, y, color, *groups, **kwargs):
        super().__init__(y, color, *groups, **kwargs)
        self.image = pygame.Surface((55, 40), pygame.SRCALPHA, 32)
        self.image.blit(load_image('images/trampoline.jpg', 55, 20), (0, 20))
        self.rect = pygame.Rect(0, 0, 55, 1)
        pygame.draw.rect(self.image, pygame.Color(color), (0, 30, 55, 10))


class Spring(Platform):
    v0y = 900

    def __init__(self, y, color, *groups, **kwargs):
        super().__init__(y, color, *groups, **kwargs)
        self.image = pygame.Surface((55, 40), pygame.SRCALPHA, 32)
        self.image.blit(load_image('images/spring.jpg', 55, 20), (0, 20))
        self.rect = pygame.Rect(0, 0, 55, 1)
        pygame.draw.rect(self.image, pygame.Color(color), (0, 30, 55, 10))
