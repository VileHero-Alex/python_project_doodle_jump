import pygame
import random
import time
from src.load_image import load_image


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, color, *group):
        super().__init__(*group)
        self.color = color
        self.block = False
        self.image = pygame.Surface((50, 10), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color(color), (0, 0, 50, 12))
        self.rect = pygame.Rect(x, y, 50, 1)
        self.time = -1

    def update(self, *game_properties):

        if self.rect.y > game_properties[0].height:
            self.image = pygame.Surface((50, 10), pygame.SRCALPHA, 32)
            pygame.draw.rect(self.image, pygame.Color(
                self.color), (0, 0, 50, 12))
            self.rect.x = random.randint(0, 300)
            x = random.randint(min(135, max(
                50, game_properties[0].h // 350)), min(135, max(50, game_properties[0].h // 350)))
            self.rect.y = game_properties[0].max_y - x
            game_properties[0].max_y = self.rect.y
            self.block = False
        else:
            self.rect.y += game_properties[0].c


class MovingPlatform(Platform):

    def update(self, *game_properties):
        self.rect.x += int(self.mv)
        if self.rect.x >= 290:
            self.mv = -1

        if self.rect.x <= 5:
            self.mv = 1

        Platform.update(self, *game_properties)


class BreakablePlatform(Platform):

    def broke(self):
        self.image = pygame.Surface((50, 10), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color("grey"), (0, 0, 15, 10))
        pygame.draw.rect(self.image, pygame.Color("grey"), (18, 0, 14, 10))
        pygame.draw.rect(self.image, pygame.Color("grey"), (35, 0, 15, 10))
        self.time = time.time()

    def destroyed(self):
        self.image = pygame.Surface((50, 10), pygame.SRCALPHA, 32)
        self.time = -1
        self.block = True


class Trampoline(Platform):
    image = load_image('images/trampoline.jpg', 55, 20)

    def update(self, *game_properties):

        if self.rect.y > game_properties[0].height:
            self.rect.x = random.randint(0, 300)
            x = random.randint(min(135, max(50, game_properties[0].h // 350)),
                               min(135, max(50, game_properties[0].h // 350)))
            self.rect.y = game_properties[0].max_y - x
            game_properties[0].max_y = self.rect.y
        else:
            self.rect.y += game_properties[0].c


class Spring(Platform):
    image = load_image('images/spring.jpg', 55, 20)

    def update(self, *game_properties):

        if self.rect.y > game_properties[0].height:
            self.rect.x = random.randint(0, 300)
            x = random.randint(min(135, max(50, game_properties[0].h // 350)),
                               min(135, max(50, game_properties[0].h // 350)))
            self.rect.y = game_properties[0].max_y - x
            game_properties[0].max_y = self.rect.y
        else:
            self.rect.y += game_properties[0].c
