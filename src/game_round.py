import pygame
import random
import time
import sys
from src.game_properties import GameProperties
from src.calculate_score import calculate_score, show_text
from src.show_start_screen import show_start_screen
from src.platforms import Platform, MovingPlatform, BreakablePlatform
from src.platforms import Spring, Trampoline
from src.ball import Ball
from src.game_over import GameOver
from src.monster import Monster
from src.player import Player
from src.sound import Sound


def game_round():
    all_sprites = pygame.sprite.Group()
    borders = pygame.sprite.Group()
    players = pygame.sprite.Group()
    balls = pygame.sprite.Group()
    monsters = pygame.sprite.Group()
    breakables = pygame.sprite.Group()
    game_properties = GameProperties()

    show_start_screen(game_properties)
    for i in range(0, 501, 50):
        Platform(i, "black", game_properties, all_sprites, borders)

    spring = Spring(-670, 'black', game_properties, all_sprites, borders)
    trampoline = Trampoline(-360, 'black',
                            game_properties, all_sprites, borders)

    break_plat1 = BreakablePlatform(
        125, "grey", game_properties, all_sprites, breakables)
    break_plat2 = BreakablePlatform(
        315, "grey", game_properties, all_sprites, breakables)
    break_plat3 = BreakablePlatform(
        435, "grey", game_properties, all_sprites, breakables)
    move_plat1 = MovingPlatform(-215, "brown",
                                game_properties, all_sprites, borders)
    move_plat2 = MovingPlatform(-425, "brown",
                                game_properties, all_sprites, borders)

    monster = Monster(-350, game_properties, all_sprites, monsters)

    player = Player(155, 300, game_properties, all_sprites, players)

    running = True
    add_score = 0
    ball_cooldown = time.time()
    while running:
        game_properties.screen.fill(((255, 255, 255)))
        calculate_score(add_score, 10, 525, 30, game_properties)
        for event in pygame.event.get():

            if event.type == pygame.QUIT or \
                    pygame.key.get_pressed()[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
            elif pygame.key.get_pressed()[pygame.K_SPACE] and \
                    time.time() - ball_cooldown > 0.1:

                x = (game_properties.width * 302120941 +
                     player.x) % game_properties.width
                Ball(x, player.y, game_properties, all_sprites, balls)
                ball_cooldown = time.time()
                Sound.shoot.play()
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            player.vx -= 2
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            player.vx += 2
        if pygame.sprite.spritecollideany(monster, players):
            running = False
        if player.y > game_properties.height:
            running = False
        if pygame.sprite.spritecollideany(monster, balls):
            monster.y -= 3500
            monster.x = random.randint(75, 275)
            add_score += 3000
        flag = False
        if pygame.sprite.spritecollideany(spring, player.sprites) and \
                player.is_flying_downwards():

            player.touch(spring.v0y)
            flag = True
            Sound.spring.play()
        elif pygame.sprite.spritecollideany(trampoline, player.sprites) and \
                player.is_flying_downwards():

            player.touch(trampoline.v0y)
            flag = True
            Sound.trampoline.play()
        if not flag:
            for breakable in breakables:
                if (pygame.sprite.spritecollideany(breakable, player.sprites)
                        and player.is_flying_downwards()):

                    breakable.broken()
                    add_score += 69
                    flag = True

        if not flag:
            for border in borders:
                if pygame.sprite.spritecollideany(border, player.sprites) and \
                        player.is_flying_downwards():

                    player.touch(Platform.v0y)
                    flag = True

        if -150 <= monster.rect.y <= 550:
            Sound.monster.play()

        game_properties.clock.tick(game_properties.FPS)
        player.update()
        all_sprites.update()
        game_properties.delta = 0
        all_sprites.draw(game_properties.screen)
        pygame.display.flip()

    player.touch(0)
    while player.y <= game_properties.height + 100:
        game_properties.screen.fill((255, 255, 255))
        player.update()
        all_sprites.update()
        game_properties.delta = 0
        all_sprites.draw(game_properties.screen)
        game_properties.clock.tick(game_properties.FPS)
        pygame.display.flip()

    gm = GameOver(all_sprites, game_properties)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:

                running = False
        if gm.rect.x == 0:
            break
        game_properties.screen.fill(pygame.Color('white'))
        all_sprites.draw(game_properties.screen)
        all_sprites.update()
        game_properties.clock.tick(game_properties.FPS)
        pygame.display.flip()

    gm.rect.x = 0
    running = True
    while running:
        for event in pygame.event.get():
            if pygame.key.get_pressed()[pygame.K_r]:
                return True
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return False
        all_sprites.update()
        game_properties.screen.fill(pygame.Color('white'))
        all_sprites.draw(game_properties.screen)
        game_properties.clock.tick(game_properties.FPS)
        calculate_score(add_score, 0, 330, 70, game_properties)
        show_text("Press R to restart", 0, 400, 40, game_properties)
        show_text("Press any other key to quit", 0, 450, 30, game_properties)
        pygame.display.flip()
