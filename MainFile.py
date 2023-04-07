import pygame
import os
import random
import time
import sys


pygame.init()
pygame.mixer.music.load('sounds/background.mp3')
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(-1)
all_sprites = pygame.sprite.Group()
borders = pygame.sprite.Group()

players = pygame.sprite.Group()

balls = pygame.sprite.Group()

monsters = pygame.sprite.Group()

clock = pygame.time.Clock()

size = 350, 550
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('white'))
jump = pygame.mixer.Sound('sounds/kick.ogg')
shoot = pygame.mixer.Sound('sounds/shoot.ogg')
tramp = pygame.mixer.Sound('sounds/trampol.ogg')
spring = pygame.mixer.Sound('sounds/springboing.ogg')
mons = pygame.mixer.Sound('sounds/monster.ogg')

def terminate():
    pygame.quit()
    sys.exit()

FPS = 50


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


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, color, group=True):
        if group:
            super().__init__(all_sprites, borders)
        else:
            super().__init__(all_sprites)
        self.color = color
        self.block = False
        self.image = pygame.Surface((50, 10), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color(color), (0, 0, 50, 12))
        self.rect = pygame.Rect(x, y, 50, 1)
        self.time = -1

    def update(self):
        global max_y

        if self.rect.y > height:
            self.image = pygame.Surface((50, 10), pygame.SRCALPHA, 32)
            pygame.draw.rect(self.image, pygame.Color(self.color), (0, 0, 50, 12))
            self.rect.x = random.randint(0, 300)
            x = random.randint(min(135, max(50, h // 350)), min(135, max(50, h // 350)))
            self.rect.y = max_y - x
            max_y = self.rect.y
            self.block = False
        else:
            self.rect.y += c


class MovingPlatform(Platform):

    def update(self):
        self.rect.x += int(self.mv)
        if self.rect.x >= 290:
            self.mv = -1

        if self.rect.x <= 5:
            self.mv = 1

        Platform.update(self)


class BrokenPlatform(Platform):

    def broke(self):
        self.image = pygame.Surface((50, 10), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color("grey"), (0, 0, 15, 10))
        pygame.draw.rect(self.image, pygame.Color("grey"), (18, 0, 14, 10))
        pygame.draw.rect(self.image, pygame.Color("grey"), (35, 0, 15, 10))
        self.time = time.time()

    def destroyed(self):
        self.image = pygame.Surface((50, 10), pygame.SRCALPHA, 32)
        self.time = -1
        self.block = True


class RECT(pygame.sprite.Sprite):

    def __init__(self, pl):
        super().__init__()
        self.rect = pl.get_rect()


class Ball(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__(all_sprites, balls)
        self.ax = x
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA, 32)
        pygame.draw.ellipse(self.image, pygame.Color("red"), (0, 0, 20, 20))
        self.rect = pygame.Rect(x, y, 40, 40)
        self.v = -1
        self.vx = 1

    def update(self):
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


class Monster(pygame.sprite.Sprite):
    image = load_image("ingameSprites/monster.png", 100, 100, (255, 255, 255))

    def __init__(self, x, y):
        super().__init__(all_sprites, monsters)
        self.image = Monster.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y
        self.ax = self.rect.x
        self.vx = 1

    def update(self):
        global max_y
        self.rect.x += self.vx
        if self.rect.x >= self.ax + 3:
            self.vx = -1
        elif self.rect.x <= self.ax - 3:
            self.vx = 1
        if self.rect.y > height:
            self.rect.x = random.randint(75, 275)
            self.ax = self.rect.x
            self.rect.y = -3160
        else:
            self.rect.y += c

    def get_rect(self):
        return pygame.Rect(self.rect.x + 3, self.rect.y, 60, 60)


class Trampoline(Platform):
    image = load_image('ingameSprites/trampoline.jpg', 55, 20)

    def update(self):
        global max_y

        if self.rect.y > height:
            self.rect.x = random.randint(0, 300)
            x = random.randint(min(135, max(50, h // 350)), min(135, max(50, h // 350)))
            self.rect.y = max_y - x
            max_y = self.rect.y
        else:
            self.rect.y += c


class Spring(Platform):
    image = load_image('ingameSprites/spring.jpg', 55, 20)
    
    def update(self):
        global max_y

        if self.rect.y > height:
            self.rect.x = random.randint(0, 300)
            x = random.randint(min(135, max(50, h // 350)), min(135, max(50, h // 350)))
            self.rect.y = max_y - x
            max_y = self.rect.y
        else:
            self.rect.y += c


class Cur(pygame.sprite.Sprite):
    image = load_image("ingameSprites/hero.jpg", 40, 40)

    def __init__(self, group, coord_x=0):
        super().__init__(players, group)
        self.image = Cur.image
        self.rect = self.image.get_rect()
        self.rect.y = 440
        self.rect.x = a + coord_x
        self.mask = pygame.mask.from_surface(self.image)
        self.k = -1
        self.p = 0

    def update(self):
        self.rect.y += self.k
        self.rect.x += left
        self.p += self.k

    def get_rect(self):
        return pygame.Rect(self.rect.x + 3, self.rect.y + 40, 34, 1)


class GameOver(pygame.sprite.Sprite):
    car_image = load_image("systemImages/GameOver.jpg", *size)

    def __init__(self, group):
        super().__init__(group)
        self.image = GameOver.car_image
        self.rect = self.image.get_rect()
        self.rect.x = -600
        self.rect.y = 0

    def update(self, *args):
        if self.rect.x < 0:
            self.rect.x += 1


def start_screen():
    s = ['systemImages/Game3.jpg', 'systemImages/Game2.jpg',
         'systemImages/Game1.jpg', 'systemImages/GameLetsGo.jpg',
         'systemImages/GameLetsGo.jpg']
    idx = 0
    fon = pygame.transform.scale(load_image(s[idx], *size), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50

    while True:
        if idx == len(s):
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return

        fon = pygame.transform.scale(load_image(s[idx], *size), (width, height))
        idx += 1
        screen.blit(fon, (0, 0))
        clock.tick(3)
        pygame.display.flip()
        clock.tick(FPS)


def score(text, x, y, size):
    intro_text = [str(text)]
    font = pygame.font.Font(None, size)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, (207, 27, 28))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.y = y
        intro_rect.x = x
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


width, height = size
running = True
x1 = 0
y1 = 0
h = 0

a = random.randint(0, width - 50)
Platform(a, 500, "black")
Platform(random.randint(0, width - 50), 0, "black")
Platform(random.randint(0, width - 50), 50, "black")
Platform(random.randint(0, width - 50), 100, "black")
Platform(random.randint(0, width - 50), 150, "black")
Platform(random.randint(0, width - 50), 250, "black")
Platform(random.randint(0, width - 50), 300, "black")
Platform(random.randint(0, width - 50), 350, "black")
Platform(random.randint(0, width - 50), 400, "black")
spr = Spring(random.randint(0, width - 50), -670, 'black')

spr.image = Spring.image
spr.rect = spr.image.get_rect()
spr.rect.y = -650
spr.rect.x = 100
trmp = Trampoline(random.randint(0, width - 50), 360, 'black')
trmp.image = Trampoline.image
trmp.rect = spr.image.get_rect()
trmp.rect.y = 200
trmp.rect.x = 100
b1 = BrokenPlatform(random.randint(0, width - 50), 125, "grey", False)
b2 = BrokenPlatform(random.randint(0, width - 50), 315, "grey", False)
b3 = BrokenPlatform(random.randint(0, width - 50), 435, "grey", False)
m1 = MovingPlatform(5, -215, "brown")
m2 = MovingPlatform(120, -425, "brown")
mnstr = Monster(random.randint(75, 275), -150)
m1.mv = 1
m2.mv = 1
max_y = 0
c = 0
left = 0
last = 550
cnt = 0
fl = True
Player1 = Cur(all_sprites)
Player2 = Cur(all_sprites, 350)
start_screen()
while running:
    screen.fill(((255, 255, 255)))
    score(cnt, 10, 525, 30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            terminate()
        if pygame.key.get_pressed()[pygame.K_SPACE]:

            x, y = Player1.rect.x, Player1.rect.y
            x1, y1 = Player2.rect.x, Player2.rect.y
            ball1 = Ball(x, y)
            ball2 = Ball(x1, y1)
            shoot.play()
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            if fl:
                fl = False
                Player1.image = pygame.transform.flip(Player1.image, True, False)
                Player2.image = pygame.transform.flip(Player1.image, True, False)
            left = -1
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            left = 1
            if not fl:
                fl = True
                Player1.image = pygame.transform.flip(Player1.image, True, False)
                Player2.image = pygame.transform.flip(Player1.image, True, False)
        else:
            left = 0
    if Player1.p < -150:
        Player1.k = 1
        Player2.k = 1
        Player1.p = 0

    if Player1.rect.y < 250:
        c = (250 - Player1.rect.y)
        cnt += c
        Player1.rect.y = 250
        Player2.rect.y = 250
        last = 250
    else:
        c = 0
    if Player1.rect.y == height:
        running = False
    if Player1.rect.y < last:
        cnt += abs(Player1.rect.y - last)
        last = Player1.rect.y

    max_y += c
    h += c
    r1 = RECT(Player1)
    r2 = RECT(Player2)
    mns = RECT(mnstr)
    if pygame.sprite.collide_rect(mnstr, Player1):
        running = False
    elif pygame.sprite.collide_rect(mnstr, Player2):
        running = False
    for ball in balls:
        if pygame.sprite.collide_rect(ball, mnstr):
            mnstr.rect.y -= 3500
            mnstr.rect.x = random.randint(75, 275)
            cnt += 3000
    if pygame.sprite.collide_rect(spr, r1) and Player1.k == 1:
        spring.play()
        Player1.k = -3
        Player1.p = 200
        Player2.k = -3
        Player2.p = 200
    elif pygame.sprite.collide_rect(spr, r2) and Player1.k == 1:
        spring.play()
        Player1.k = -3
        Player1.p = 200
        Player2.k = -3
        Player2.p = 200
    elif pygame.sprite.collide_rect(trmp, r1) and Player1.k == 1:
        tramp.play()
        Player1.k = -2
        Player1.p = 150
        Player2.k = -2
        Player2.p = 150
    elif pygame.sprite.collide_rect(trmp, r2) and Player1.k == 1:
        tramp.play()
        Player1.k = -2
        Player1.p = 150
        Player2.k = -2
        Player2.p = 150
    elif pygame.sprite.collide_rect(b1, r1) and Player1.k > 0 and not b1.block:
        b1.broke()
    elif pygame.sprite.collide_rect(b2, r1) and Player1.k > 0 and not b2.block:
        b2.broke()
    elif pygame.sprite.collide_rect(b1, r2) and Player1.k > 0 and not b1.block:
        b1.broke()
    elif pygame.sprite.collide_rect(b2, r2) and Player1.k > 0 and not b2.block:
        b2.broke()
    elif pygame.sprite.collide_rect(b3, r1) and Player1.k > 0 and not b3.block:
        b3.broke()
    elif pygame.sprite.collide_rect(b3, r2) and Player1.k > 0 and not b3.block:
        b3.broke()
    elif (len(pygame.sprite.spritecollide(r1, borders, False)) == 1 and Player1.k == 1)\
            or (len(pygame.sprite.spritecollide(r2, borders, False)) == 1 and Player2.k == 1):
        jump.play()
        Player1.k = -1
        Player2.k = -1
        Player1.p = 0
        Player2.p = 0
        time.sleep(0.05)

    if b1.time != -1 and time.time() - b1.time >= 0.5:
        b1.destroyed()

    if b2.time != -1 and time.time() - b2.time >= 0.5:
        b2.destroyed()

    if b3.time != -1 and time.time() - b3.time >= 0.5:
        b3.destroyed()

    if -150 <= mnstr.rect.y <= 550:
        mons.play()

    Player2.rect.x = (Player1.rect.x + 350) % 350
    clock.tick(200)

    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()

c = 0
while Player1.rect.y <= 580 or Player2.rect.y <= 580:
    screen.fill((255, 255, 255))
    left = 0
    Player1.rect.y += 1
    Player2.rect.y += 1
    all_sprites.draw(screen)
    clock.tick(200)
    pygame.display.flip()

gm = GameOver(all_sprites)
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

    all_sprites.update()
    screen.fill(pygame.Color('white'))
    all_sprites.draw(screen)
    all_sprites.update()
    clock.tick(200)
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

    all_sprites.update()
    screen.fill(pygame.Color('white'))
    all_sprites.draw(screen)
    all_sprites.update()
    clock.tick(200)
    score(cnt, 0, 330, 70)
    pygame.display.flip()

pygame.quit()