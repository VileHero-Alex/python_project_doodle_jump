import pygame


class Sound():
    pygame.init()
    pygame.mixer.music.load('sounds/background.ogg')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    jump = pygame.mixer.Sound('sounds/kick.ogg')
    shoot = pygame.mixer.Sound('sounds/shoot.ogg')
    trampoline = pygame.mixer.Sound('sounds/trampol.ogg')
    spring = pygame.mixer.Sound('sounds/springboing.ogg')
    monster = pygame.mixer.Sound('sounds/monster.ogg')
