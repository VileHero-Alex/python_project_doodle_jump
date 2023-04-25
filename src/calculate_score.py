import pygame


def calculate_score(number, x, y, size, game_properties):
    line = str(int(number + game_properties.record_height))
    text = "Score: " + line
    show_text(text, x, y, size, game_properties)


def show_text(text, x, y, size, game_properties):
    font = pygame.font.Font(None, size)
    text_coord = 50
    string_rendered = font.render(text, 1, (207, 27, 28))
    intro_rect = string_rendered.get_rect()
    text_coord += 10
    intro_rect.top = text_coord
    intro_rect.y = y
    intro_rect.x = x
    text_coord += intro_rect.height
    game_properties.screen.blit(string_rendered, intro_rect)
