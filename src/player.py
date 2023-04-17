import pygame
from src.load_image import load_image


class Player(pygame.sprite.Sprite):
    image = load_image("images/hero.jpg", 40, 40)

    def __init__(self, a, *groups, coord_x=0):
        super().__init__(*groups)
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.rect.y = 440
        self.rect.x = a + coord_x
        self.mask = pygame.mask.from_surface(self.image)
        self.k = -1
        self.p = 0

    def update(self, *game_properties):
        self.rect.y += self.k
        self.rect.x += game_properties[0].left
        self.p += self.k

    def get_rect(self):
        return pygame.Rect(self.rect.x + 3, self.rect.y + 40, 34, 1)
