import pygame
import os
from random import choice
from math import asin, pi, sqrt, sin, cos, atan
import sys
import sqlite3

pygame.mixer.init()
pygame.init()
BUILDED = pygame.mixer.Sound('data/sound/builded.wav')
BOOM = pygame.mixer.Sound('data/sound/boom.wav')
BUL = pygame.mixer.Sound('data/sound/bul.wav')
NEEDDOLD = pygame.mixer.Sound('data/sound/neeggold.wav')
MONEY = pygame.mixer.Sound('data/sound/money.wav')
ZOMBI = pygame.mixer.Sound('data/sound/zomb.wav')
BUILD = pygame.mixer.Sound('data/sound/build.wav')
MINUSHEART = pygame.mixer.Sound('data/sound/minusheart.wav')
ROAD = [[[1080, 120, -5, 0, 0], [320, 120, 3, 5, 1], [500, 420, -4, 5, 1],
         [436, 500, -3, -1, 0],
         [49, 371, 0, 0, 0], [50, 372]],
        [[1080, 280, -5, 0, 0], [380, 280, 3, 4, 1], [500, 440, -4, 5, 1],
         [436, 520, -3, -1, 0],
         [49, 391, 0, 0, 0], [50, 392]]]
ROAD2 = [[[1080, 120, -10, 0, 0], [320, 120, 6, 10, 1], [500, 420, -8, 10, 1],
          [436, 500, -6, -2, 0],
          [52, 372, 0, 0, 0], [50, 372]],
         [[1080, 280, -10, 0, 0], [380, 280, 6, 8, 1], [500, 440, -8, 10, 1],
          [436, 520, -6, -2, 0],
          [52, 392, 0, 0, 0], [53, 393]]]
COOR_BUILD = [(250, 140), (360, 65), (500, 225), (800, 370), (575, 375),
              (250, 550), (220, 370),
              (310, 390)]
V = 500
size = width, height = 1080, 720
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
running_menu = True
check_pause = False
check_restart = False
check_pause_draw = True
check_exit = False
return_to_menu = False


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def count_coords(x1, y1, x2, y2):
    d_x = x2 - x1
    d_y = y2 - y1
    typ = None
    if d_x <= 0 and d_y <= 0:
        d_x = - d_x
        d_y = - d_y
        typ = 2
    elif d_x >= 0 and d_y >= 0:
        typ = 4
    elif d_x < 0 and d_y > 0:
        d_x = - d_x
        typ = 3
    elif d_x > 0 and d_y < 0:
        d_y = - d_y
        typ = 1
    if d_x == 0:
        angle = pi / 2
    elif d_y == 0:
        angle = 0
    else:
        angle = atan(d_y / d_x)
    d_types = {1: 2 * pi - angle, 2: pi + angle, 3: pi - angle, 4: angle}
    return d_types[typ]


class Game_over_anim:
    image = load_image('game_over_image.png')
    image = pygame.transform.scale(image, (1080, 720))

    def __init__(self):
        super().__init__()
        self.pos = [-1080, 0]
        self.image = Game_over_anim.image

    def draw(self):
        screen.blit(self.image, (self.pos[0], self.pos[1]))

    def update(self):
        if self.pos[0] != 0:
            self.pos[0] += 1
            return True
        if self.pos[0] == 0:
            return False


class Player:
    def __init__(self):
        self.heart = 1
        self.money = 200
        self.points = 0
        self.image_heart = load_image('menu_in_game/heart.png', (255, 255, 255))
        self.image_heart = pygame.transform.scale(self.image_heart, (90, 60))
        self.image_money = load_image('menu_in_game/money.jpg', (255, 255, 255))
        self.image_money = pygame.transform.scale(self.image_money, (50, 50))

    def draw(self):
        screen.blit(self.image_heart, (50, -5))
        screen.blit(self.image_money, (200, 0))
        font = pygame.font.Font(None, 50)
        text = font.render(str(self.heart), 1, (255, 255, 255))
        screen.blit(text, (120, 10))
        text = font.render(str(self.money), 1, (255, 255, 255))
        screen.blit(text, (250, 10))


class Gun(pygame.sprite.Sprite):
    image_1 = load_image('gun_and_boom/gun.png', (255, 255, 255))
    image_1 = pygame.transform.scale(image_1, (25, 25))
    image_2 = load_image('gun_and_boom/boom.png')
    image_2 = pygame.transform.scale(image_2, (50, 50))

    def __init__(self, group, *args):
        BUL.play()
        super().__init__(group)
        self.image = self.image_1
        self.rect = self.image.get_rect()
        self.rect.x = args[0]
        self.rect.y = args[1]
        self.boom = False
        self.i = 0
        self.dx = V // 100 * cos(args[2])
        self.dy = V // 100 * sin(args[2])

    def update(self, gun_sprites):
        if self.boom:
            if self.i == 0:
                BOOM.play()
                self.image = Gun.image_2
            self.i += 1
            if self.i == 50:
                gun_sprites.remove(self)
        else:
            self.rect.x += self.dx
            self.rect.y += self.dy


class Tower_and_build(pygame.sprite.Sprite):
    image = load_image("tower_and_build/tower_and_build1.png")
    image = pygame.transform.scale(image, (50, 50))
    image_move_1 = load_image("tower_and_build/tower_and_build1_move.png")
    image_move_1 = pygame.transform.scale(image_move_1, (50, 50))
    image2 = load_image("tower_and_build/tower_and_build2.png")
    image2 = pygame.transform.scale(image2, (50, 50))
    image_move_2 = load_image("tower_and_build/tower_and_build2_move.png")
    image_move_2 = pygame.transform.scale(image_move_2, (50, 50))
    image3 = load_image("tower_and_build/tower_and_build3.png")
    image3 = pygame.transform.scale(image3, (50, 50))
    image_move_3 = load_image("tower_and_build/tower_and_build3_move.png")
    image_move_3 = pygame.transform.scale(image_move_3, (50, 50))
    image4 = load_image("tower_and_build/towerkiano.png")
    image4 = pygame.transform.scale(image4, (75, 150))
    images = [image, image2, image3, image_move_1, image_move_2, image_move_3,
              image4]

    def __init__(self, group, pos):
        super().__init__(group)
        self.checkcount = 0
        self.change = False
        self.startbuild = False
        self.built = False
        self.status = "UP"
        self.statusi = 0
        self.image = Tower_and_build.images[self.statusi]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def get_click(self, pos, player):
        if self.rect.x <= pos[0] and self.rect.y <= pos[1] and self.rect.x + \
                self.rect.size[0] >= \
                pos[0] and self.rect.y + self.rect.size[1] >= pos[1] and not (
                self.built):
            if player.money >= 100 and not (self.startbuild):
                self.startbuild = True
                BUILD.play()
                player.money -= 100
            elif self.startbuild:
                pass
            else:
                NEEDDOLD.play()

    def update(self):
        if self.change:
            self.image = self.images[self.statusi + 3]
        else:
            if self.built:
                self.image = self.images[-1]
            else:
                self.image = self.images[self.statusi]

    def check_change(self, pos):
        if self.rect.x <= pos[0] and self.rect.y <= pos[1] and self.rect.x + \
                self.rect.size[0] >= \
                pos[0] and self.rect.y + self.rect.size[1] >= pos[1] and not (
                self.built):
            self.change = True
        else:
            self.change = False

    def builds(self):
        if self.startbuild:
            if self.checkcount == 4:
                self.built = True
                self.change = False
                self.startbuild = False
                self.rect.x -= 0
                self.rect.y -= 70
                BUILDED.play()
            else:
                self.checkcount += 1
                if self.status == "UP":
                    self.statusi += 1
                    if self.statusi == 2:
                        self.status = "DOWN"
                else:
                    self.statusi -= 1
                    if self.statusi == 0:
                        self.status = "UP"


class Evil(pygame.sprite.Sprite):
    image = load_image('Evil/evil.png', (255, 255, 255))
    image2 = load_image('Evil/evil2.png', (255, 255, 255))
    image = pygame.transform.scale(image, (75, 75))
    image2 = pygame.transform.scale(image2, (75, 75))
    image = pygame.transform.flip(image, True, False)
    image2 = pygame.transform.flip(image2, True, False)

    def __init__(self, group):
        super().__init__(group)
        self.coords = ROAD[choice([0, 1])]
        self.pos = 0
        self.hp = 70
        self.image1 = Evil.image
        self.image2 = Evil.image2
        self.image = self.image1
        self.rect = self.image2.get_rect()
        self.rect.x, self.rect.y, self.d_x, self.d_y, flip = self.coords[
            self.pos]
        ZOMBI.play()

    def update(self, gun_sprites, Evil_sprites, player):
        self.image = self.image2 if self.image == self.image1 else self.image1
        if self.rect.x == self.coords[self.pos + 1][0] and self.rect.y == \
                self.coords[self.pos + 1][1]:
            self.pos += 1
            self.rect.x, self.rect.y, self.d_x, self.d_y, flip = self.coords[
                self.pos]
            self.image1 = pygame.transform.flip(self.image1, flip, 0)
            self.image2 = pygame.transform.flip(self.image2, flip, 0)
        self.rect.x += self.d_x
        self.rect.y += self.d_y
        a = pygame.sprite.spritecollide(self, gun_sprites, False)
        if a:
            if a[0].boom == False:
                a[0].boom = True
                self.hp -= 10
        if self.hp == 0:
            MONEY.play()
            Evil_sprites.remove(self)
            player.money += 20
            player.points += 1


class Evil2(pygame.sprite.Sprite):
    image = load_image('Evil2/evil.png', (255, 255, 255))
    image2 = load_image('Evil2/evil2.png', (255, 255, 255))
    image = pygame.transform.scale(image, (105, 70))
    image2 = pygame.transform.scale(image2, (105, 70))
    image = pygame.transform.flip(image, True, False)
    image2 = pygame.transform.flip(image2, True, False)

    def __init__(self, group):
        super().__init__(group)
        self.coords = ROAD2[choice([0, 1])]
        self.pos = 0
        self.hp = 30
        self.image1 = Evil2.image
        self.image2 = Evil2.image2
        self.image = self.image1
        self.rect = self.image2.get_rect()
        self.rect.x, self.rect.y, self.d_x, self.d_y, flip = self.coords[
            self.pos]

    def update(self, gun_sprites, Evil2_sprites, player):
        self.image = self.image2 if self.image == self.image1 else self.image1
        if self.rect.x == self.coords[self.pos + 1][0] and self.rect.y == \
                self.coords[self.pos + 1][1]:
            self.pos += 1
            self.rect.x, self.rect.y, self.d_x, self.d_y, flip = self.coords[
                self.pos]
            self.image1 = pygame.transform.flip(self.image1, flip, 0)
            self.image2 = pygame.transform.flip(self.image2, flip, 0)
        self.rect.x += self.d_x
        self.rect.y += self.d_y
        a = pygame.sprite.spritecollide(self, gun_sprites, False)
        if a:
            if a[0].boom == False:
                a[0].boom = True
                self.hp -= 10
        if self.hp == 0:
            Evil2_sprites.remove(self)
            MONEY.play()
            player.money += 10
            player.points += 1


class Pause(pygame.sprite.Sprite):
    pause = load_image("menu_in_game/menu_pause.png")
    pause = pygame.transform.scale(pause, (50, 50))

    def __init__(self, group):
        super().__init__(group)
        self.image = Pause.pause
        self.rect = self.image.get_rect()
        self.rect.x = 1030
        self.rect.y = 0

    def get_click(self, pos):
        if self.rect.x <= pos[0] and self.rect.y <= pos[1] and self.rect.x + \
                self.rect.size[0] >= \
                pos[0] and self.rect.y + self.rect.size[1] >= pos[1]:
            return True
        return False


class Continue(pygame.sprite.Sprite):
    continue_btn = load_image("pause/continue.png")
    continue_btn = pygame.transform.scale(continue_btn, (200, 50))

    def __init__(self, group):
        super().__init__(group)
        self.image = Continue.continue_btn
        self.rect = self.image.get_rect()
        self.rect.x = 450
        self.rect.y = 500

    def get_click(self, pos):
        if self.rect.x <= pos[0] and self.rect.y <= pos[1] and self.rect.x + \
                self.rect.size[0] >= \
                pos[0] and self.rect.y + self.rect.size[1] >= pos[1]:
            return False
        return True


class Restart(pygame.sprite.Sprite):
    restart_btn = load_image("pause/restart.png")
    restart_btn = pygame.transform.scale(restart_btn, (200, 250))

    def __init__(self, group):
        super().__init__(group)
        self.image = Restart.restart_btn
        self.rect = self.image.get_rect()
        self.rect.x = 450
        self.rect.y = 200

    def get_click(self, pos):
        if self.rect.x <= pos[0] and self.rect.y <= pos[1] and self.rect.x + \
                self.rect.size[0] >= \
                pos[0] and self.rect.y + self.rect.size[1] >= pos[1]:
            return True
        return False


class Exit(pygame.sprite.Sprite):
    exit_btn = load_image("pause/exit.png", (255, 255, 255))
    exit_btn = pygame.transform.scale(exit_btn, (200, 175))

    def __init__(self, group):
        super().__init__(group)
        self.image = Exit.exit_btn
        self.rect = self.image.get_rect()
        self.rect.x = 475
        self.rect.y = 550

    def get_click(self, pos):
        if self.rect.x <= pos[0] and self.rect.y <= pos[1] and self.rect.x + \
                self.rect.size[0] >= \
                pos[0] and self.rect.y + self.rect.size[1] >= pos[1]:
            return True
        return False


class Backgroung:
    def __init__(self):
        self.image = load_image("fonmain.png")
        self.image = pygame.transform.scale(self.image, (1080, 720))

    def draw(self):
        screen.blit(self.image, (0, 0))


class City:
    image = load_image("city/city1.png")
    image = pygame.transform.scale(image, (1080, 720))
    image2 = load_image("city/city2.png")
    image2 = pygame.transform.scale(image2, (1080, 720))
    image3 = load_image("city/city3.png")
    image3 = pygame.transform.scale(image3, (1080, 720))
    images = [image, image2, image3]

    def __init__(self):
        self.status = "UP"
        self.statusi = 1
        self.image = City.images[self.statusi]
        screen.blit(self.image, (0, 0))

    def cheageimage(self):
        if self.status == "UP":
            self.statusi += 1
            if self.statusi == 2:
                self.status = "DOWN"
        else:
            self.statusi -= 1
            if self.statusi == 0:
                self.status = "UP"
        self.image = City.images[self.statusi]

    def draw(self):
        screen.blit(self.image, (0, 0))


class Sea:
    image = load_image("sea/sea1.png")
    image = pygame.transform.scale(image, (1080, 720))
    image2 = load_image("sea/sea2.png")
    image2 = pygame.transform.scale(image2, (1080, 720))
    image3 = load_image("sea/sea3.png")
    image3 = pygame.transform.scale(image3, (1080, 720))
    images = [image, image2, image3]

    def __init__(self):
        self.status = "UP"
        self.statusi = 1
        self.image = Sea.images[self.statusi]
        screen.blit(self.image, (0, 0))

    def cheageimage(self):
        if self.status == "UP":
            self.statusi += 1
            if self.statusi == 2:
                self.status = "DOWN"
        else:
            self.statusi -= 1
            if self.statusi == 0:
                self.status = "UP"
        self.image = Sea.images[self.statusi]

    def draw(self):
        screen.blit(self.image, (0, 0))


class Electro:
    image = load_image("electro/electro1.png")
    image = pygame.transform.scale(image, (1080, 720))
    image2 = load_image("electro/electro2.png")
    image2 = pygame.transform.scale(image2, (1080, 720))
    image3 = load_image("electro/electro3.png")
    image3 = pygame.transform.scale(image3, (1080, 720))
    images = [image, image2, image3]

    def __init__(self):
        self.status = "UP"
        self.statusi = 1
        self.image = Electro.images[self.statusi]
        screen.blit(self.image, (0, 0))

    def cheageimage(self):
        if self.status == "UP":
            self.statusi += 1
            if self.statusi == 2:
                self.status = "DOWN"
        else:
            self.statusi -= 1
            if self.statusi == 0:
                self.status = "UP"
        self.image = Electro.images[self.statusi]

    def draw(self):
        screen.blit(self.image, (0, 0))


class BackgroundMenu:
    def __init__(self):
        self.image = load_image("menu/fonmenu.png")
        self.image = pygame.transform.scale(self.image, (1080, 720))

    def draw(self):
        screen.blit(self.image, (0, 0))


class NameMenu:
    def __init__(self):
        self.image = load_image("menu/name.png", (255, 255, 255))
        self.image = pygame.transform.scale(self.image, (1080, 720))

    def draw(self):
        screen.blit(self.image, (30, 0))


class AuthorMenu:
    def __init__(self):
        self.image = load_image("menu/text5.png", (255, 255, 255))
        self.image = pygame.transform.scale(self.image, (108, 72))

    def draw(self):
        screen.blit(self.image, (972, 670))


class StartMenu(pygame.sprite.Sprite):
    image_start = load_image('menu/text1.png', (255, 255, 255))
    image_start = pygame.transform.scale(image_start, (300, 150))

    def __init__(self, group):
        super().__init__(group)
        self.image = StartMenu.image_start
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 150

    def update(self, *args):
        if args and args[
            0].type == pygame.MOUSEMOTION and self.rect.collidepoint(
            args[0].pos):
            self.image = pygame.transform.scale(StartMenu.image_start,
                                                (400, 200))
        elif args and args[
            0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(
            args[0].pos):
            levels()
        else:
            self.image = pygame.transform.scale(StartMenu.image_start,
                                                (300, 150))


class EndMenu(pygame.sprite.Sprite):
    image_end = load_image('menu/text2.png', (255, 255, 255))
    image_end = pygame.transform.scale(image_end, (300, 150))

    def __init__(self, group):
        super().__init__(group)
        self.image = EndMenu.image_end
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 550

    def update(self, *args):
        if args and args[
            0].type == pygame.MOUSEMOTION and self.rect.collidepoint(
            args[0].pos):
            self.image = pygame.transform.scale(EndMenu.image_end,
                                                (400, 200))
        elif args and args[
            0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(
            args[0].pos):
            pygame.quit()
            sys.exit(0)
        else:
            self.image = pygame.transform.scale(EndMenu.image_end,
                                                (300, 150))


class Records(pygame.sprite.Sprite):
    image_records = load_image('menu/text4.png', (255, 255, 255))
    image_records = pygame.transform.scale(image_records, (300, 150))

    def __init__(self, group):
        super().__init__(group)
        self.image = Records.image_records
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 350

    def update(self, *args):
        if args and args[
            0].type == pygame.MOUSEMOTION and self.rect.collidepoint(
            args[0].pos):
            self.image = pygame.transform.scale(Records.image_records,
                                                (400, 200))
        else:
            self.image = pygame.transform.scale(Records.image_records,
                                                (300, 150))


class NameLevels:
    def __init__(self):
        self.image = load_image("menu/levels.png", (255, 255, 255))
        self.image = pygame.transform.scale(self.image, (540, 360))

    def draw(self):
        screen.blit(self.image, (360, 0))


class Level1(pygame.sprite.Sprite):
    image_level_1 = load_image('menu/level1.png', (255, 255, 255))
    image_level_1 = pygame.transform.scale(image_level_1, (300, 150))

    def __init__(self, group):
        super().__init__(group)
        self.image = Level1.image_level_1
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 150

    def update(self, *args):
        if args and args[
            0].type == pygame.MOUSEMOTION and self.rect.collidepoint(
            args[0].pos):
            self.image = pygame.transform.scale(Level1.image_level_1,
                                                (400, 200))
        elif args and args[
            0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(
            args[0].pos):
            name()
        else:
            self.image = pygame.transform.scale(Level1.image_level_1,
                                                (300, 150))


class Back(pygame.sprite.Sprite):
    image_back = load_image('menu/back.png', (255, 255, 255))
    image_back = pygame.transform.scale(image_back, (300, 150))

    def __init__(self, group):
        super().__init__(group)
        self.image = Back.image_back
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 550

    def update(self, *args):
        global return_to_menu
        if args and args[
            0].type == pygame.MOUSEMOTION and self.rect.collidepoint(
            args[0].pos):
            self.image = pygame.transform.scale(Back.image_back,
                                                (400, 200))
        elif args and args[
            0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(
            args[0].pos):
            return_to_menu = True
        else:
            self.image = pygame.transform.scale(Back.image_back,
                                                (300, 150))


class Level2(pygame.sprite.Sprite):
    image_level_2 = load_image('menu/level2.png', (255, 255, 255))
    image_level_2 = pygame.transform.scale(image_level_2, (300, 150))

    def __init__(self, group):
        super().__init__(group)
        self.image = Level2.image_level_2
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 350

    def update(self, *args):
        if args and args[
            0].type == pygame.MOUSEMOTION and self.rect.collidepoint(
            args[0].pos):
            self.image = pygame.transform.scale(Level2.image_level_2,
                                                (400, 200))
        else:
            self.image = pygame.transform.scale(Level2.image_level_2,
                                                (300, 150))


def game(text):
    global check_pause
    global check_pause_draw
    global check_restart
    global check_exit
    towers = []
    evils = []
    tower_sprites_1 = pygame.sprite.Group()
    backgroung_image = Backgroung()
    cityo = City()
    electroo = Electro()
    seao = Sea()
    Cityanim = 1
    Seaanim = 2
    Electroanim = 3
    Buildanim = 10
    MoveEvil = 30
    AddEvil = 28
    AddEvil2 = 18
    player = Player()
    Evil_sprites = pygame.sprite.Group()
    Evil2_sprites = pygame.sprite.Group()
    menu = pygame.sprite.Group()
    menu_pause = pygame.sprite.Group()
    menu_restart = pygame.sprite.Group()
    menu_exit = pygame.sprite.Group()
    gun_sprites = pygame.sprite.Group()
    Hit = 29
    MoveGun = 27
    for i in range(8):
        a = Tower_and_build(tower_sprites_1, COOR_BUILD[i])
        towers.append(a)
    Pause(menu)
    Continue(menu_pause)
    Restart(menu_restart)
    Exit(menu_exit)
    a = Evil(Evil_sprites)
    evils.append(a)
    a = Evil2(Evil2_sprites)
    evils.append(a)
    pygame.time.set_timer(Cityanim, 1000)
    pygame.time.set_timer(Seaanim, 2000)
    pygame.time.set_timer(Electroanim, 100)
    pygame.time.set_timer(MoveEvil, 100)
    pygame.time.set_timer(AddEvil, 2000)
    pygame.time.set_timer(AddEvil2, 1000)
    pygame.time.set_timer(Buildanim, 1000)
    pygame.time.set_timer(Hit, 1000)
    pygame.time.set_timer(MoveGun, 5)
    running = True
    while running:
        if check_pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for i in menu_pause:
                            check_pause = i.get_click(event.pos)
                        for i in menu_restart:
                            check_restart = i.get_click(event.pos)
                            if check_restart:
                                check_pause = False
                        for i in menu_exit:
                            check_exit = i.get_click(event.pos)
                            if check_exit:
                                check_pause = False

            if check_pause_draw:
                screen.blit(load_image("pause/fon_pause.png"), (0, 0))
                font = pygame.font.Font(None, 50)
                text = font.render(str("Menu"), 1, (0, 0, 0))
                screen.blit(text, (500, 10))
                check_pause_draw = False
            menu_pause.draw(screen)
            menu_restart.draw(screen)
            menu_exit.draw(screen)
        else:
            if check_restart or check_exit:
                check_pause = False
                check_restart = False
                check_pause_draw = True
                if check_exit:
                    check_exit = False
                    return
                towers = []
                evils = []
                tower_sprites_1 = pygame.sprite.Group()
                backgroung_image = Backgroung()
                cityo = City()
                electroo = Electro()
                seao = Sea()
                player = Player()
                Evil_sprites = pygame.sprite.Group()
                Evil2_sprites = pygame.sprite.Group()
                menu = pygame.sprite.Group()
                menu_pause = pygame.sprite.Group()
                menu_restart = pygame.sprite.Group()
                a = Evil(Evil_sprites)
                evils.append(a)
                a = Evil2(Evil2_sprites)
                evils.append(a)
                gun_sprites = pygame.sprite.Group()
                for i in range(8):
                    a = Tower_and_build(tower_sprites_1, COOR_BUILD[i])
                    towers.append(a)
                Pause(menu)
                Continue(menu_pause)
                Restart(menu_restart)
            check_pause_draw = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == Cityanim:
                    cityo.cheageimage()
                if event.type == Seaanim:
                    seao.cheageimage()
                if event.type == Electroanim:
                    electroo.cheageimage()
                if event.type == MoveEvil:
                    Evil_sprites.update(gun_sprites, Evil_sprites, player)
                    for evil in Evil_sprites:
                        if evil.rect.x == 49 and (
                                evil.rect.y == 371 or evil.rect.y == 391):
                            Evil_sprites.remove(evil)
                            MINUSHEART.play()
                            player.heart -= 1
                    Evil2_sprites.update(gun_sprites, Evil2_sprites, player)
                    for evil2 in Evil2_sprites:
                        if evil2.rect.x == 52 and (
                                evil2.rect.y == 372 or evil2.rect.y == 392):
                            Evil2_sprites.remove(evil2)
                            MINUSHEART.play()
                            player.heart -= 1
                    if player.heart < 1:
                        runnin = True
                        game_over = Game_over_anim()
                        while runnin:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    runnin = False
                            clock.tick(200)
                            game_over.draw()
                            pygame.display.flip()
                            runnin = game_over.update()
                        con = sqlite3.connect("data/record.db")
                        cur = con.cursor()
                        result = cur.execute("""SELECT player FROM Free_mode""").fetchall()
                        if text not in [i[0] for i in result]:
                            print(1)
                            cur.execute(f"""INSERT
                                           INTO
                                           Free_mode(player, Best_Points, Last_points)
                                           VALUES('{text}', {player.points}, {player.points})""")
                        else:
                            cur.execute(f"""UPDATE Free_mode
                                            SET Last_points = {player.points}
                                            WHERE player = '{text}'""")
                            if player.points > int(cur.execute(
                                    f"""SELECT Best_Points FROM Free_mode WHERE player = '{text}'""").fetchone()[
                                                       0]):
                                cur.execute(f"""UPDATE fFree_mode
                                                SET Best_Points = {player.points}
                                                WHERE player = '{text}'""")
                        con.commit()
                        con.close()
                        check_exit = True
                if event.type == AddEvil:
                    a = Evil(Evil_sprites)
                    evils.append(a)
                if event.type == AddEvil2:
                    a = Evil2(Evil2_sprites)
                    evils.append(a)
                if event.type == Buildanim:
                    for i in towers:
                        i.builds()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for i in towers:
                            i.get_click(event.pos, player)
                        for i in menu:
                            check_pause = i.get_click(event.pos)
                if event.type == pygame.MOUSEMOTION:
                    for i in towers:
                        i.check_change(event.pos)
                if event.type == Hit:
                    for build in tower_sprites_1:
                        if build.built:
                            hit_done = False
                            x1, y1 = build.rect.x, build.rect.y
                            for evil in Evil_sprites:
                                x2, y2 = evil.rect.x, evil.rect.y
                                if (x2 - x1) ** 2 + (y2 - y1) ** 2 <= 30000:
                                    angle = count_coords(x1 + 20, y1 + 20,
                                                         x2 + 30,
                                                         y2 + 30)
                                    if angle:
                                        Gun(gun_sprites, x1 + 20, y1 + 20,
                                            angle)
                                        hit_done = True
                                        break
                            if not hit_done:
                                for evil2 in Evil2_sprites:
                                    x2, y2 = evil2.rect.x, evil2.rect.y
                                    if (x2 - x1) ** 2 + (
                                            y2 - y1) ** 2 <= 30000:
                                        angle = count_coords(x1 + 20, y1 + 20,
                                                             x2 + 30,
                                                             y2 + 30)
                                        if angle:
                                            Gun(gun_sprites, x1 + 20, y1 + 20,
                                                angle)
                                            break

                if event.type == MoveGun:
                    gun_sprites.update(gun_sprites)
            backgroung_image.draw()
            player.draw()
            cityo.draw()
            seao.draw()
            electroo.draw()
            Evil_sprites.draw(screen)
            Evil2_sprites.draw(screen)
            gun_sprites.draw(screen)
            tower_sprites_1.draw(screen)
            menu.draw(screen)
            tower_sprites_1.update()
        pygame.display.flip()
        clock.tick(10000)
    pygame.quit()


def levels():
    global return_to_menu
    running_levels = True
    while running_levels:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_levels = False
            level_1_sprite.update(event)
            level_2_sprite.update(event)
            back_sprite.update(event)
            if return_to_menu:
                return_to_menu = False
                return
        backgroung_menu_image.draw()
        name_levels.draw()
        level_1_sprite.draw(screen)
        level_2_sprite.draw(screen)
        back_sprite.draw(screen)
        pygame.display.flip()
        clock.tick(10000)
    pygame.quit()


def name():
    global return_to_menu
    nicname = ''
    running_levels = True
    while running_levels:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_levels = False
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[13]:
                    game(nicname)
                    return_to_menu = True
                elif keys[pygame.K_BACKSPACE]:
                    nicname = nicname[:-1]
                elif len(nicname) < 30:
                    nicname += event.unicode
            back_sprite.update(event)
            if return_to_menu:
                return_to_menu = False
                return
        backgroung_menu_image.draw()
        font = pygame.font.Font(None, 50)
        text = font.render(str("Введите имя"), 1, (0, 0, 0))
        screen.blit(text, (400, 10))
        font = pygame.font.Font(None, 50)
        text = font.render(str(nicname), 1, (0, 0, 0))
        screen.blit(text, (400, 100))
        back_sprite.draw(screen)
        pygame.display.flip()
        clock.tick(10000)
    pygame.quit()


if __name__ == '__main__':
    name_menu = NameMenu()
    author_menu = AuthorMenu()
    name_levels = NameLevels()
    end_menu_sprite = pygame.sprite.Group()
    start_menu_sprite = pygame.sprite.Group()
    StartMenu(start_menu_sprite)
    EndMenu(end_menu_sprite)
    records_sprite = pygame.sprite.Group()
    Records(records_sprite)
    level_1_sprite = pygame.sprite.Group()
    level_2_sprite = pygame.sprite.Group()
    back_sprite = pygame.sprite.Group()
    backgroung_menu_image = BackgroundMenu()
    Level1(level_1_sprite)
    Level2(level_2_sprite)
    Back(back_sprite)

    while running_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_menu = False
            start_menu_sprite.update(event)
            end_menu_sprite.update(event)
            records_sprite.update(event)
        backgroung_menu_image.draw()
        name_menu.draw()
        author_menu.draw()
        start_menu_sprite.draw(screen)
        end_menu_sprite.draw(screen)
        records_sprite.draw(screen)
        pygame.display.flip()
        clock.tick(10000)
    pygame.quit()
