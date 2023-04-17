import pygame


class Ball(pygame.sprite.Sprite):

    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.ax = x
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA, 32)
        pygame.draw.ellipse(self.image, pygame.Color("red"), (0, 0, 20, 20))
        self.rect = pygame.Rect(x, y, 40, 40)
        self.v = -1
        self.vx = 1

    def update(self, *game_properties):
        self.rect.y += self.v
        self.rect.x += self.vx
        if self.rect.x >= self.ax + 10:
            self.vx = -1
        if self.rect.x <= self.ax - 10:
            self.vx = 1
        if self.rect.y <= -20:
            self.rect.x = 400
            self.vx = 0
            self.v = 0
