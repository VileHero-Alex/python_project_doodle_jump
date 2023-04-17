import pygame
import sys
from src.load_image import load_image


def show_start_screen(game_properties):
    s = ['images/Game3.jpg', 'images/Game2.jpg',
         'images/Game1.jpg', 'images/GameLetsGo.jpg',
         'images/GameLetsGo.jpg']
    idx = 0
    fon = pygame.transform.scale(load_image(
        s[idx], *game_properties.size), (game_properties.width, game_properties.height))
    game_properties.screen.blit(fon, (0, 0))

    while True:
        if idx == len(s):
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return

        fon = pygame.transform.scale(
            load_image(s[idx], *game_properties.size), (game_properties.width, game_properties.height))
        idx += 1
        game_properties.screen.blit(fon, (0, 0))
        game_properties.clock.tick(3)
        pygame.display.flip()
        game_properties.clock.tick(game_properties.FPS)
