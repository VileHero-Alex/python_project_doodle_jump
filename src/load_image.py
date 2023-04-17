import pygame
import os


def load_image(name, scx, scy, colorkey=None):
    fullname = os.path.join(name)
    image = pygame.image.load(fullname)
    image = image.convert_alpha()
    image = pygame.transform.scale(image, (scx, scy))
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image
