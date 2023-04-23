import pygame
from src.game_round import game_round
from src.sound import Sound

running = True
while running:
    running = game_round()

pygame.quit()
