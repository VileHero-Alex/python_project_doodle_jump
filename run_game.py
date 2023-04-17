from src.calculate_score import calculate_score
from src.start_screen import show_start_screen
from src.game_over import GameOver

from src.game_properties import GameProperties

game_properties = GameProperties()

from src.monster import Monster
from src.player import Player
from src.rectangular_base import RectangularBase
from src.ball import Ball
from src.platforms import Platform, MovingPlatform, BreakablePlatform, Spring, Trampoline
from src.load_image import load_image
import pygame
import random
import time
import sys


pygame.init()
pygame.mixer.music.load('sounds/background.ogg')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)
jump_sound = pygame.mixer.Sound('sounds/kick.ogg')
shoot_sound = pygame.mixer.Sound('sounds/shoot.ogg')
trampoline_sound = pygame.mixer.Sound('sounds/trampol.ogg')
spring_sound = pygame.mixer.Sound('sounds/springboing.ogg')
monster_sound = pygame.mixer.Sound('sounds/monster.ogg')

all_sprites = pygame.sprite.Group()
borders = pygame.sprite.Group()
players = pygame.sprite.Group()
balls = pygame.sprite.Group()
monsters = pygame.sprite.Group()


running = True


a = random.randint(0, game_properties.width - 50)
Platform(a, 500, "black", all_sprites, borders)
for i in range(0, 401, 50):
    Platform(random.randint(0, game_properties.width - 50),
             i, "black", all_sprites, borders)

spring_object = Spring(random.randint(
    0, game_properties.width - 50), -670, 'black', all_sprites, borders)
spring_object.image = Spring.image
spring_object.rect = spring_object.image.get_rect()
spring_object.rect.y = -650
spring_object.rect.x = 100

trampoline_object = Trampoline(random.randint(
    0, game_properties.width - 50), 360, 'black', all_sprites, borders)
trampoline_object.image = Trampoline.image
trampoline_object.rect = spring_object.image.get_rect()
trampoline_object.rect.y = 200
trampoline_object.rect.x = 100

break_plat1 = BreakablePlatform(
    random.randint(0, game_properties.width - 50), 125, "grey", all_sprites)
break_plat2 = BreakablePlatform(
    random.randint(0, game_properties.width - 50), 315, "grey", all_sprites)
break_plat3 = BreakablePlatform(
    random.randint(0, game_properties.width - 50), 435, "grey", all_sprites)
move_plat1 = MovingPlatform(5, -215, "brown", all_sprites, borders)
move_plat2 = MovingPlatform(120, -425, "brown", all_sprites, borders)

monster = Monster(random.randint(75, 275), -150, all_sprites, monsters)

player1 = Player(a, all_sprites, players)
player2 = Player(a, all_sprites, players, coord_x=350)

move_plat1.mv = 1
move_plat2.mv = 1
game_properties.left = 0
last = 550
cnt = 0
fl = True

show_start_screen(game_properties)

while running:
    game_properties.screen.fill(((255, 255, 255)))
    calculate_score(cnt, 10, 525, 30, game_properties)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            x, y = player1.rect.x, player1.rect.y
            x1, y1 = player2.rect.x, player2.rect.y
            ball1 = Ball(x, y, all_sprites, balls)
            ball2 = Ball(x1, y1, all_sprites, balls)
            shoot_sound.play()
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            if fl:
                fl = False
                player1.image = pygame.transform.flip(
                    player1.image, True, False)
                player2.image = pygame.transform.flip(
                    player1.image, True, False)
            game_properties.left = -1
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            game_properties.left = 1
            if not fl:
                fl = True
                player1.image = pygame.transform.flip(
                    player1.image, True, False)
                player2.image = pygame.transform.flip(
                    player1.image, True, False)
        else:
            game_properties.left = 0
    if player1.p < -150:
        player1.k = 1
        player2.k = 1
        player1.p = 0

    if player1.rect.y < 250:
        game_properties.c = (250 - player1.rect.y)
        cnt += game_properties.c
        player1.rect.y = 250
        player2.rect.y = 250
        last = 250
    else:
        game_properties.c = 0
    if player1.rect.y == game_properties.height:
        running = False
    if player1.rect.y < last:
        cnt += abs(player1.rect.y - last)
        last = player1.rect.y

    game_properties.max_y += game_properties.c
    game_properties.h += game_properties.c

    rect_player1 = RectangularBase(player1)
    rect_player2 = RectangularBase(player2)

    if pygame.sprite.collide_rect(monster, player1):
        running = False
    elif pygame.sprite.collide_rect(monster, player2):
        running = False
    for ball in balls:
        if pygame.sprite.collide_rect(ball, monster):
            monster.rect.y -= 3500
            monster.rect.x = random.randint(75, 275)
            cnt += 3000
    if pygame.sprite.collide_rect(spring_object, rect_player1) and player1.k == 1:
        spring_sound.play()
        player1.k = -3
        player1.p = 200
        player2.k = -3
        player2.p = 200
    elif pygame.sprite.collide_rect(spring_object, rect_player2) and player1.k == 1:
        spring_sound.play()
        player1.k = -3
        player1.p = 200
        player2.k = -3
        player2.p = 200
    elif pygame.sprite.collide_rect(trampoline_object, rect_player1) and player1.k == 1:
        trampoline_sound.play()
        player1.k = -2
        player1.p = 150
        player2.k = -2
        player2.p = 150
    elif pygame.sprite.collide_rect(trampoline_object, rect_player2) and player1.k == 1:
        trampoline_sound.play()
        player1.k = -2
        player1.p = 150
        player2.k = -2
        player2.p = 150
    elif pygame.sprite.collide_rect(break_plat1, rect_player1) and player1.k > 0 and not break_plat1.block:
        break_plat1.broke()
    elif pygame.sprite.collide_rect(break_plat2, rect_player1) and player1.k > 0 and not break_plat2.block:
        break_plat2.broke()
    elif pygame.sprite.collide_rect(break_plat1, rect_player2) and player1.k > 0 and not break_plat1.block:
        break_plat1.broke()
    elif pygame.sprite.collide_rect(break_plat2, rect_player2) and player1.k > 0 and not break_plat2.block:
        break_plat2.broke()
    elif pygame.sprite.collide_rect(break_plat3, rect_player1) and player1.k > 0 and not break_plat3.block:
        break_plat3.broke()
    elif pygame.sprite.collide_rect(break_plat3, rect_player2) and player1.k > 0 and not break_plat3.block:
        break_plat3.broke()
    elif (len(pygame.sprite.spritecollide(rect_player1, borders, False)) == 1 and player1.k == 1)\
            or (len(pygame.sprite.spritecollide(rect_player2, borders, False)) == 1 and player2.k == 1):
        jump_sound.play()
        player1.k = -1
        player2.k = -1
        player1.p = 0
        player2.p = 0
        time.sleep(0.05)

    if break_plat1.time != -1 and time.time() - break_plat1.time >= 0.5:
        break_plat1.destroyed()

    if break_plat2.time != -1 and time.time() - break_plat2.time >= 0.5:
        break_plat2.destroyed()

    if break_plat3.time != -1 and time.time() - break_plat3.time >= 0.5:
        break_plat3.destroyed()

    if -150 <= monster.rect.y <= 550:
        monster_sound.play()

    player2.rect.x = (player1.rect.x + 350) % 350
    game_properties.clock.tick(200)

    all_sprites.draw(game_properties.screen)
    all_sprites.update(game_properties)
    pygame.display.flip()

game_properties.c = 0
while player1.rect.y <= 580 or player2.rect.y <= 580:
    game_properties.screen.fill((255, 255, 255))
    left = 0
    player1.rect.y += 1
    player2.rect.y += 1
    all_sprites.draw(game_properties.screen)
    game_properties.clock.tick(200)
    pygame.display.flip()

gm = GameOver(all_sprites, game_properties)
running = True
fl = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            fl = True
    if fl:
        fl = False
        continue
    if gm.rect.x == 0:
        break

    all_sprites.update(game_properties)
    game_properties.screen.fill(pygame.Color('white'))
    all_sprites.draw(game_properties.screen)
    all_sprites.update(game_properties)
    game_properties.clock.tick(200)
    pygame.display.flip()

running = True
fl = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            running = False
    if fl:
        fl = False
        continue

    all_sprites.update(game_properties)
    game_properties.screen.fill(pygame.Color('white'))
    all_sprites.draw(game_properties.screen)
    all_sprites.update(game_properties)
    game_properties.clock.tick(200)
    calculate_score(cnt, 0, 330, 70, game_properties)
    pygame.display.flip()

pygame.quit()
