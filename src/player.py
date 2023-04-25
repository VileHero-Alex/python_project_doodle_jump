import pygame
import time
from src.load_image import load_image


class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, shift, width, player, *groups):
        super().__init__(*groups)
        self.player = player
        self.image = load_image("images/hero.jpg", 40, 40)
        self.rect = pygame.Rect(player.x, player.y, 40, 20)

        self.shift = shift
        self.width = width

    def update(self):
        if int(self.player.x) + self.shift > 2 * self.width:
            self.shift -= 3 * self.width
        if int(self.player.x) + self.shift < -self.width:
            self.shift += 3 * self.width
        self.rect.x = int(self.player.x) + self.shift
        self.rect.y = int(self.player.y)


class Player():
    def __init__(self, x, y, game_properties, all_sprites, player_sprites):
        self.ax, self.ay = 0.7, 500
        self.v0y = 0
        self.x, self.y, self.y0 = x, y, y
        self.vx = 0
        self.orientation = 1
        self.sprites = []
        width = game_properties.width
        for shift in range(-width, width + 1, width):
            self.sprites.append(PlayerSprite(
                shift, width, self, all_sprites, player_sprites,))
        self.game_properties = game_properties
        self.last_touch = time.time()

    def decelerate(self):
        self.x += self.vx
        if self.orientation == 1 and self.vx < 0 or \
                self.orientation == -1 and self.vx > 0:
            
            self.orientation = -self.orientation
            for sprite in self.sprites:
                sprite.image = pygame.transform.flip(sprite.image, True, False)
        self.vx = 0

    def update(self):
        delta_time = time.time() - self.last_touch
        self.y = self.y0 - self.v0y * delta_time + self.ay * delta_time ** 2 / 2
        self.decelerate()
        self.x += self.vx * delta_time
        if self.y < 200:
            self.game_properties.delta = 200 - self.y
            self.game_properties.record_height += self.game_properties.delta
            self.y = 200
            self.y0 += self.game_properties.delta

    def touch(self, v0y):
        self.last_touch = time.time()
        self.y0 = self.y
        self.v0y = v0y

    def is_flying_downwards(self):
        return self.last_touch + self.v0y / self.ay < time.time()
