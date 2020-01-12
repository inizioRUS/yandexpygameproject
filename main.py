import pygame
import os
from random import choice
from math import asin, pi, sqrt, sin, cos, atan
import sys
from PIL import Image, ImageFilter
import sqlite3
import random

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
MUSIC = pygame.mixer.Sound('data/sound/music.wav')
MUSIC_check = False
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
COOR_BUILD_PRE = [(500, 280), (720, 130), (1000, 450), (1600, 740), (1150, 750),
                  (500, 1100), (440, 740),
                  (620, 780)]
V1 = 20000
V2 = 10000
V = 500
V_E = 1
Y = - 60
X = - 45
size = width, height = 1080, 720
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
running_menu = True
check_pause = False
check_restart = False
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
    image_pre = pygame.transform.scale(image, (100, 100))

    def __init__(self, group, pos, flag=True):
        super().__init__(group)
        if flag:
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
        else:
            self.image = Tower_and_build.image_pre
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

    def __init__(self, group, check, args):
        super().__init__(group)
        if check:
            self.coords = args
        else:
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

    def update(self, gun_sprites, Evil_sprites, player, event1, event2):
        global V1, V2
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
            if player.points % 10 == 0:
                V1 = V1 // 2
                V2 = V2 // 2
                pygame.time.set_timer(event1, V1)
                pygame.time.set_timer(event2, V2)


class Evil2(pygame.sprite.Sprite):
    image = load_image('Evil2/evil.png', (255, 255, 255))
    image2 = load_image('Evil2/evil2.png', (255, 255, 255))
    image = pygame.transform.scale(image, (105, 70))
    image2 = pygame.transform.scale(image2, (105, 70))
    image = pygame.transform.flip(image, True, False)
    image2 = pygame.transform.flip(image2, True, False)

    def __init__(self, group, check, args):
        super().__init__(group)
        if check:
            self.coords = args
            self.coords = list(
                map(lambda x: [x[0], x[1], x[2] * 2, x[3] * 2, x[4]],
                    self.coords))
        else:
            self.coords = ROAD2[choice([0, 1])]

        self.pos = 0
        self.hp = 30
        self.image1 = Evil2.image
        self.image2 = Evil2.image2
        self.image = self.image1
        self.rect = self.image2.get_rect()
        self.rect.x, self.rect.y, self.d_x, self.d_y, flip = self.coords[
            self.pos]

    def update(self, gun_sprites, Evil2_sprites, player, event1, event2):
        global V1, V2
        self.image = self.image2 if self.image == self.image1 else self.image1
        if (self.rect.x == self.coords[self.pos + 1][0] or self.rect.x ==
            self.coords[self.pos + 1][0] - 1) and (
                self.rect.y == self.coords[self.pos + 1][1] or self.rect.y ==
                self.coords[self.pos + 1][1] - 1):
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
            if player.points % 10 == 0:
                V1 = V1 // 2
                V2 = V2 // 2
                pygame.time.set_timer(event1, V1)
                pygame.time.set_timer(event2, V2)


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
    exit_btn = pygame.transform.scale(exit_btn, (200, 50))

    def __init__(self, group):
        super().__init__(group)
        self.image = Exit.exit_btn
        self.rect = self.image.get_rect()
        self.rect.x = 450
        self.rect.y = 575

    def get_click(self, pos):
        if self.rect.x <= pos[0] and self.rect.y <= pos[1] and self.rect.x + \
                self.rect.size[0] >= \
                pos[0] and self.rect.y + self.rect.size[1] >= pos[1]:
            return True
        return False


class Backgroung:
    def __init__(self, flag=True):
        self.x = 0
        self.y = 0
        if flag:
            self.image = load_image("fonmain.png")
            self.image = pygame.transform.scale(self.image, (1080, 720))
        else:
            self.image = load_image("fonmain.png")
            self.image = pygame.transform.scale(self.image, (2160, 1440))

    def draw(self, clear=False):
        if clear:
            self.image = load_image("background.jpg")
            self.image = pygame.transform.scale(self.image, (1080, 720))
            screen.blit(self.image, (0, 0))
        else:
            screen.blit(self.image, (self.x, self.y))


class City:
    image = load_image("city/city1.png")
    image = pygame.transform.scale(image, (1080, 720))
    image2 = load_image("city/city2.png")
    image2 = pygame.transform.scale(image2, (1080, 720))
    image3 = load_image("city/city3.png")
    image3 = pygame.transform.scale(image3, (1080, 720))
    images = [image, image2, image3]
    pre_preview = pygame.transform.scale(image, (2160, 1440))
    pre_preview2 = pygame.transform.scale(image2, (2160, 1440))
    pre_preview3 = pygame.transform.scale(image3, (2160, 1440))
    images2 = [pre_preview, pre_preview2, pre_preview3]

    def __init__(self, flag=True):
        self.x = 0
        self.y = 0
        self.flag = flag
        self.status = "UP"
        self.statusi = 1
        if self.flag:
            self.image = City.images[self.statusi]
        else:
            self.image = City.images2[self.statusi]
        screen.blit(self.image, (self.x, self.y))

    def cheageimage(self):
        if self.status == "UP":
            self.statusi += 1
            if self.statusi == 2:
                self.status = "DOWN"
        else:
            self.statusi -= 1
            if self.statusi == 0:
                self.status = "UP"
        if self.flag:
            self.image = City.images[self.statusi]
        else:
            self.image = City.images2[self.statusi]

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


class Sea:
    image = load_image("sea/sea1.png")
    image = pygame.transform.scale(image, (1080, 720))
    image2 = load_image("sea/sea2.png")
    image2 = pygame.transform.scale(image2, (1080, 720))
    image3 = load_image("sea/sea3.png")
    image3 = pygame.transform.scale(image3, (1080, 720))
    images = [image, image2, image3]
    pre_preview = pygame.transform.scale(image, (2160, 1440))
    pre_preview2 = pygame.transform.scale(image2, (2160, 1440))
    pre_preview3 = pygame.transform.scale(image3, (2160, 1440))
    images2 = [pre_preview, pre_preview2, pre_preview3]

    def __init__(self, flag=True):
        self.x = 0
        self.y = 0
        self.flag = flag
        self.status = "UP"
        self.statusi = 1
        if self.flag:
            self.image = Sea.images[self.statusi]
        else:
            self.image = Sea.images2[self.statusi]
        screen.blit(self.image, (self.x, self.y))

    def cheageimage(self):
        if self.status == "UP":
            self.statusi += 1
            if self.statusi == 2:
                self.status = "DOWN"
        else:
            self.statusi -= 1
            if self.statusi == 0:
                self.status = "UP"
        if self.flag:
            self.image = Sea.images[self.statusi]
        else:
            self.image = Sea.images2[self.statusi]

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


class Electro:
    image = load_image("electro/electro1.png")
    image = pygame.transform.scale(image, (1080, 720))
    image2 = load_image("electro/electro2.png")
    image2 = pygame.transform.scale(image2, (1080, 720))
    image3 = load_image("electro/electro3.png")
    image3 = pygame.transform.scale(image3, (1080, 720))
    images = [image, image2, image3]
    pre_preview = pygame.transform.scale(image, (2160, 1440))
    pre_preview2 = pygame.transform.scale(image2, (2160, 1440))
    pre_preview3 = pygame.transform.scale(image3, (2160, 1440))
    images2 = [pre_preview, pre_preview2, pre_preview3]

    def __init__(self, flag=True):
        self.x = 0
        self.y = 0
        self.flag = flag
        self.status = "UP"
        self.statusi = 1
        if self.flag:
            self.image = Electro.images[self.statusi]
        else:
            self.image = Electro.images2[self.statusi]
        screen.blit(self.image, (self.x, self.y))

    def cheageimage(self):
        if self.status == "UP":
            self.statusi += 1
            if self.statusi == 2:
                self.status = "DOWN"
        else:
            self.statusi -= 1
            if self.statusi == 0:
                self.status = "UP"
        if self.flag:
            self.image = Electro.images[self.statusi]
        else:
            self.image = Electro.images2[self.statusi]

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


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


class StartMenu:
    image_start = load_image('menu/text1.png', (255, 255, 255))
    image_start = pygame.transform.scale(image_start, (300, 150))

    def __init__(self):
        self.check_size = False
        self.image = StartMenu.image_start
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 400

    def update(self, *args):
        if args and args[
            0].type == pygame.MOUSEMOTION and self.rect.collidepoint(
            args[0].pos):
            self.check_size = True
        elif args and args[
            0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(
            args[0].pos):
            levels()
        elif args and args[
            0].type == pygame.MOUSEMOTION and not (self.rect.collidepoint(
            args[0].pos)):
            self.check_size = False

    def draw(self):
        if self.check_size:
            screen.blit(pygame.transform.scale(StartMenu.image_start,
                                               (400, 200)), (self.rect.x, self.rect.y))
        else:
            screen.blit(pygame.transform.scale(StartMenu.image_start,
                                               (300, 150)), (self.rect.x, self.rect.y))


class EndMenu:
    image_end = load_image('menu/text2.png', (255, 255, 255))
    image_end = pygame.transform.scale(image_end, (300, 150))

    def __init__(self):
        self.check_size = False
        self.image = EndMenu.image_end
        self.rect = self.image.get_rect()
        self.rect.x = 750
        self.rect.y = 400

    def update(self, *args):
        if args and args[
            0].type == pygame.MOUSEMOTION and self.rect.collidepoint(
            args[0].pos):
            self.check_size = True
        elif args and args[
            0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(
            args[0].pos):
            pygame.quit()
            sys.exit(0)
        elif args and args[
            0].type == pygame.MOUSEMOTION and not (self.rect.collidepoint(
            args[0].pos)):
            self.check_size = False

    def draw(self):
        if self.check_size:
            screen.blit(pygame.transform.scale(EndMenu.image_end,
                                               (400, 200)), (self.rect.x, self.rect.y))
        else:
            screen.blit(pygame.transform.scale(EndMenu.image_end,
                                               (300, 150)), (self.rect.x, self.rect.y))


class Records:
    image_records = load_image('menu/text4.png', (255, 255, 255))
    image_records = pygame.transform.scale(image_records, (300, 150))

    def __init__(self):
        self.check_size = False
        self.image = Records.image_records
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 400

    def update(self, *args):
        if args and args[
            0].type == pygame.MOUSEMOTION and self.rect.collidepoint(
            args[0].pos):
            self.check_size = True
        elif args and args[
            0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(
            args[0].pos):
            record()
        elif args and args[
            0].type == pygame.MOUSEMOTION and not (self.rect.collidepoint(
            args[0].pos)):
            self.check_size = False

    def draw(self):
        if self.check_size:
            screen.blit(pygame.transform.scale(Records.image_records,
                                               (400, 200)), (self.rect.x, self.rect.y))
        else:
            screen.blit(pygame.transform.scale(Records.image_records,
                                               (300, 150)), (self.rect.x, self.rect.y))


class NameLevels:
    def __init__(self):
        self.image = load_image("menu/levels.png", (255, 255, 255))
        self.image = pygame.transform.scale(self.image, (540, 360))

    def draw(self):
        screen.blit(self.image, (250, -120))


class Level1:
    image_level_1 = load_image('menu/level1.png', (255, 255, 255))
    image_level_1 = pygame.transform.scale(image_level_1, (300, 150))

    def __init__(self):
        self.check_size = False
        self.image = Level1.image_level_1
        self.rect = self.image.get_rect()
        self.rect.x = 150
        self.rect.y = 300

    def update(self, *args):
        if args and args[
            0].type == pygame.MOUSEMOTION and self.rect.collidepoint(
            args[0].pos):
            self.check_size = True
        elif args and args[
            0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(
            args[0].pos):
            name(1)
        elif args and args[
            0].type == pygame.MOUSEMOTION and not (self.rect.collidepoint(
            args[0].pos)):
            self.check_size = False

    def draw(self):
        if self.check_size:
            screen.blit(pygame.transform.scale(Level1.image_level_1,
                                               (400, 200)), (self.rect.x, self.rect.y))
        else:
            screen.blit(pygame.transform.scale(Level1.image_level_1,
                                               (300, 150)), (self.rect.x, self.rect.y))


class Back:
    image_back = load_image('menu/back.png', (255, 255, 255))
    image_back = pygame.transform.scale(image_back, (300, 150))

    def __init__(self):
        self.check_size = False
        self.image = Back.image_back
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 550

    def update(self, *args):
        global return_to_menu
        if args and args[
            0].type == pygame.MOUSEMOTION and self.rect.collidepoint(
            args[0].pos):
            self.check_size = True
        elif args and args[
            0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(
            args[0].pos):
            return_to_menu = True
        elif args and args[
            0].type == pygame.MOUSEMOTION and not (self.rect.collidepoint(
            args[0].pos)):
            self.check_size = False

    def draw(self):
        if self.check_size:
            screen.blit(pygame.transform.scale(Back.image_back,
                                               (400, 200)), (self.rect.x, self.rect.y))
        else:
            screen.blit(pygame.transform.scale(Back.image_back,
                                               (300, 150)), (self.rect.x, self.rect.y))


class Level2:
    image_level_2 = load_image('menu/level2.png', (255, 255, 255))
    image_level_2 = pygame.transform.scale(image_level_2, (300, 150))

    def __init__(self):
        self.check_size = False
        self.image = Level1.image_level_1
        self.rect = self.image.get_rect()
        self.rect.x = 600
        self.rect.y = 300

    def update(self, *args):
        if args and args[
            0].type == pygame.MOUSEMOTION and self.rect.collidepoint(
            args[0].pos):
            self.check_size = True
        elif args and args[
            0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(
            args[0].pos):
            name(2)
        elif args and args[
            0].type == pygame.MOUSEMOTION and not (self.rect.collidepoint(
            args[0].pos)):
            self.check_size = False

    def draw(self):
        if self.check_size:
            screen.blit(pygame.transform.scale(Level2.image_level_2,
                                               (400, 200)), (self.rect.x, self.rect.y))
        else:
            screen.blit(pygame.transform.scale(Level2.image_level_2,
                                               (300, 150)), (self.rect.x, self.rect.y))


class Road(pygame.sprite.Sprite):
    horizontal_image = load_image('create_road/stright_.png', (255, 255, 255))
    vertical_image = load_image('create_road/stright_.png', (255, 255, 255))
    vertical_image = pygame.transform.rotate(vertical_image, 90)
    rotate_image = load_image('create_road/rotate_new.png', (255, 255, 255))

    def __init__(self, group1, group2, group3, mod, x1, y1, x2=0, y2=0, rotate=0, road='left'):
        if mod == 'h':
            super().__init__(group1)
            self.image = Road.horizontal_image
            self.rect = self.image.get_rect()
            self.image = pygame.transform.scale(self.image,
                                                (x2 - x1, self.rect.h))
            self.rect.x = x1
            self.rect.y = y1 - self.rect.h // 2
        elif mod == 'v':
            super().__init__(group2)
            self.image = Road.vertical_image
            self.rect = self.image.get_rect()
            self.image = pygame.transform.scale(self.image,
                                                (self.rect.w, y2 - y1))
            if road == 'left':
                self.rect.x = x1 - self.rect.w // 2
                self.rect.y = y1
            else:
                self.rect.x = x2 - self.rect.w // 2
                self.rect.y = y1

        elif mod == 'r':
            super().__init__(group3)
            self.image = Road.rotate_image
            self.rect = self.image.get_rect()
            if rotate == 180:
                self.image = pygame.transform.rotate(self.image, 180)
                self.rect.x, self.rect.y = x1 - self.rect.w * 0.75, y1 - self.rect.h * 0.75
            elif rotate == 0:
                self.rect.x, self.rect.y = x1 - self.rect.w * 0.25, y1 - self.rect.h * 0.25
            elif rotate == 270:
                self.image = pygame.transform.rotate(self.image, 270)
                self.rect.x, self.rect.y = x1 - self.rect.w * 0.7, y1 - self.rect.h * 0.25
            elif rotate == 90:
                self.image = pygame.transform.rotate(self.image, 90)
                self.rect.x, self.rect.y = x1 - self.rect.w * 0.22, y1 - self.rect.h * 0.8


class Tree(pygame.sprite.Sprite):
    image = load_image('trees.png', (255, 255, 255))
    image = pygame.transform.scale(image, (75, 150))

    def __init__(self, group, road_sprites_horizontal, road_sprites_rotate, road_sprites_vertical,
                 tower_sprites_1):
        super().__init__(group)
        self.image = Tree.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(250, size[0] - self.rect.w)
        self.rect.y = random.randrange(size[1] - self.rect.h)

        while pygame.sprite.spritecollideany(self,
                                             road_sprites_horizontal) or pygame.sprite.spritecollideany(
            self, road_sprites_rotate) or pygame.sprite.spritecollideany(
            self, road_sprites_vertical) or pygame.sprite.spritecollideany(
            self, tower_sprites_1):
            self.rect.x = random.randrange(250, size[0] - self.rect.w)
            self.rect.y = random.randrange(size[1] - self.rect.h)


def pre_Preview(nicname):
    global MUSIC_check
    MUSIC_check = False
    MUSIC.stop()
    check_up = False
    check_down = False
    check_right = False
    check_left = False
    Cityanim = 1
    Seaanim = 2
    Electroanim = 3
    pygame.time.set_timer(Cityanim, 1000)
    pygame.time.set_timer(Seaanim, 2000)
    pygame.time.set_timer(Electroanim, 100)
    tower_sprites_1 = pygame.sprite.Group()
    backgroung_image = Backgroung(False)
    cityo = City(False)
    electroo = Electro(False)
    seao = Sea(False)
    for i in range(8):
        a = Tower_and_build(tower_sprites_1, COOR_BUILD_PRE[i], False)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == Cityanim:
                cityo.cheageimage()
            if event.type == Seaanim:
                seao.cheageimage()
            if event.type == Electroanim:
                electroo.cheageimage()
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP] or event.unicode in ['w', 'W', 'ц', 'Ц']:
                    if backgroung_image.y < 0:
                        for i in tower_sprites_1:
                            i.rect.y += 20
                        cityo.y += 20
                        seao.y += 20
                        electroo.y += 20
                        backgroung_image.y += 20
                if keys[pygame.K_DOWN] or event.unicode in ['s', 'S', 'ы', 'Ы']:
                    if backgroung_image.y > - 720:
                        for i in tower_sprites_1:
                            i.rect.y -= 20
                        cityo.y -= 20
                        seao.y -= 20
                        electroo.y -= 20
                        backgroung_image.y -= 20
                if keys[pygame.K_RIGHT] or event.unicode in ['В', 'в', 'd', 'D']:
                    if backgroung_image.x > -1080:
                        for i in tower_sprites_1:
                            i.rect.x -= 20
                        cityo.x -= 20
                        seao.x -= 20
                        electroo.x -= 20
                        backgroung_image.x -= 20
                if keys[pygame.K_LEFT] or event.unicode in ['A', 'a', 'ф', 'Ф']:
                    if backgroung_image.x < 0:
                        for i in tower_sprites_1:
                            i.rect.x += 20
                        cityo.x += 20
                        seao.x += 20
                        electroo.x += 20
                        backgroung_image.x += 20
                if keys[13]:
                    game(nicname)
                    return
            if event.type == pygame.MOUSEMOTION:
                check_left = True if event.pos[0] < 54 else False
                check_right = True if event.pos[0] > 1026 else False
                check_up = True if event.pos[1] < 36 else False
                check_down = True if event.pos[1] > 684 else False
        if check_left:
            if backgroung_image.x < 0:
                for i in tower_sprites_1:
                    i.rect.x += 10
                cityo.x += 10
                seao.x += 10
                electroo.x += 10
                backgroung_image.x += 10
        if check_right:
            if backgroung_image.x > -1080:
                for i in tower_sprites_1:
                    i.rect.x -= 10
                cityo.x -= 10
                seao.x -= 10
                electroo.x -= 10
                backgroung_image.x -= 10
        if check_down:
            if backgroung_image.y > - 720:
                for i in tower_sprites_1:
                    i.rect.y -= 10
                cityo.y -= 10
                seao.y -= 10
                electroo.y -= 10
                backgroung_image.y -= 10
        if check_up:
            if backgroung_image.y < 0:
                for i in tower_sprites_1:
                    i.rect.y += 10
                cityo.y += 10
                seao.y += 10
                electroo.y += 10
                backgroung_image.y += 10
        backgroung_image.draw()
        cityo.draw()
        seao.draw()
        electroo.draw()
        tower_sprites_1.draw(screen)
        font = pygame.font.Font("data/8693.ttf", 55)
        text = font.render(str("Предпросмотр карты"), 1, (255, 229, 0))
        screen.blit(text, (300, 10))
        screen.blit(pygame.transform.scale(load_image("menu/enter.png"), (200, 75)), (850, 600))
        font = pygame.font.Font("data/8693.ttf", 20)
        text = font.render(str("Начать игру"), 1, (255, 229, 0))
        screen.blit(text, (860, 675))
        pygame.display.flip()
        clock.tick(10000)
    pygame.quit()


def game(nicname):
    global V1, V2
    global check_pause
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
    a = Evil(Evil_sprites, False, [])
    evils.append(a)
    a = Evil2(Evil2_sprites, False, [])
    evils.append(a)
    pygame.time.set_timer(Cityanim, 1000)
    pygame.time.set_timer(Seaanim, 2000)
    pygame.time.set_timer(Electroanim, 100)
    pygame.time.set_timer(MoveEvil, 100)
    pygame.time.set_timer(AddEvil, V1)
    pygame.time.set_timer(AddEvil2, V2)
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
            screen.blit(load_image("pause/fon_pause.png"), (0, 0))
            font = pygame.font.Font("data/8693.ttf", 50)
            text = font.render(str("Меню"), 1, (255, 229, 0))
            screen.blit(text, (500, 10))
            menu_pause.draw(screen)
            menu_exit.draw(screen)
            menu_restart.draw(screen)
        else:
            if check_restart or check_exit:
                V1, V2 = 20000, 10000
                pygame.time.set_timer(AddEvil, V1)
                pygame.time.set_timer(AddEvil2, V2)
                check_pause = False
                check_restart = False
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
                a = Evil(Evil_sprites, False, [])
                evils.append(a)
                a = Evil2(Evil2_sprites, False, [])
                evils.append(a)
                gun_sprites = pygame.sprite.Group()
                for i in range(8):
                    a = Tower_and_build(tower_sprites_1, COOR_BUILD[i])
                    towers.append(a)
                Pause(menu)
                Continue(menu_pause)
                Restart(menu_restart)
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
                    Evil_sprites.update(gun_sprites, Evil_sprites, player, AddEvil, AddEvil2)
                    for evil in Evil_sprites:
                        if evil.rect.x == 49 and (
                                evil.rect.y == 371 or evil.rect.y == 391):
                            Evil_sprites.remove(evil)
                            MINUSHEART.play()
                            player.heart -= 1
                    Evil2_sprites.update(gun_sprites, Evil2_sprites, player, AddEvil, AddEvil2)
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
                        if nicname not in [i[0] for i in result]:
                            cur.execute(f"""INSERT
                                           INTO
                                           Free_mode(player, Best_Points, Last_points)
                                           VALUES('{nicname}', {player.points}, {player.points})""")
                        else:
                            cur.execute(f"""UPDATE Free_mode
                                            SET Last_points = {player.points}
                                            WHERE player = '{nicname}'""")
                            if player.points > int(cur.execute(
                                    f"""SELECT Best_Points FROM Free_mode WHERE player = '{nicname}'""").fetchone()[
                                                       0]):
                                cur.execute(f"""UPDATE Free_mode
                                                SET Best_Points = {player.points}
                                                WHERE player = '{nicname}'""")
                        con.commit()
                        con.close()
                        check_exit = True
                if event.type == AddEvil:
                    a = Evil(Evil_sprites, False, [])
                    evils.append(a)
                if event.type == AddEvil2:
                    a = Evil2(Evil2_sprites, False, [])
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
    global MUSIC_check
    global return_to_menu
    running_levels = True
    while running_levels:
        if not (MUSIC_check):
            MUSIC.play()
            MUSIC_check = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_levels = False
            level1.update(event)
            level2.update(event)
            back.update(event)
            if return_to_menu:
                return_to_menu = False
                return
        backgroung_menu_image.draw()
        name_levels.draw()
        level1.draw()
        level2.draw()
        back.draw()
        pygame.display.flip()
        clock.tick(10000)
    pygame.quit()


def name(level):
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
                    if level == 1:
                        pre_Preview(nicname)
                        return_to_menu = True
                    else:
                        input_file(nicname)
                        return_to_menu = True
                elif keys[pygame.K_BACKSPACE]:
                    nicname = nicname[:-1]
                elif len(nicname) < 25:
                    nicname += event.unicode

            back.update(event)
            if return_to_menu:
                return_to_menu = False
                return
        backgroung_menu_image.draw()
        font = pygame.font.Font("data/8693.ttf", 55)
        text = font.render(str("Введите имя"), 1, (255, 229, 0))
        screen.blit(pygame.transform.scale(load_image("menu/enter.png"), (200, 75)), (850, 600))
        pygame.draw.lines(screen, (255, 229, 0), False, [(200, 450), (860, 450)])
        screen.blit(text, (410, 10))
        font = pygame.font.Font(None, 55)
        text = font.render(str(nicname), 1, (255, 229, 0))
        screen.blit(text, (200, 400))
        font = pygame.font.Font("data/8693.ttf", 20)
        text = font.render(str("Подтвердить данные"), 1, (255, 229, 0))
        screen.blit(text, (860, 675))
        back.draw()
        pygame.display.flip()
        clock.tick(10000)
    pygame.quit()


def input_file(nicname):
    global return_to_menu
    file = ''
    running_levels = True
    while running_levels:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_levels = False
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[13]:
                    draw_level(file, nicname)
                    return_to_menu = True
                elif keys[pygame.K_BACKSPACE]:
                    file = file[:-1]
                elif len(file) < 25:
                    file += event.unicode

            back.update(event)
            if return_to_menu:
                return_to_menu = False
                return
        backgroung_menu_image.draw()
        font = pygame.font.Font("data/8693.ttf", 55)
        text = font.render(str("Введите название файла"), 1, (255, 229, 0))
        screen.blit(pygame.transform.scale(load_image("menu/enter.png"), (200, 75)), (850, 600))
        pygame.draw.lines(screen, (255, 229, 0), False, [(200, 450), (860, 450)])
        screen.blit(text, (300, 10))
        font = pygame.font.Font(None, 55)
        text = font.render(str(file), 1, (255, 229, 0))
        screen.blit(text, (200, 400))
        font = pygame.font.Font("data/8693.ttf", 20)
        text = font.render(str("Подтвердить данные"), 1, (255, 229, 0))
        screen.blit(text, (860, 675))
        back.draw()
        pygame.display.flip()
        clock.tick(10000)
    pygame.quit()


def record():
    free = True
    check_right = False
    check_left = False
    global return_to_menu
    running_levels = True
    while running_levels:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_levels = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[1] < 47:
                    if event.pos[0] < 552:
                        free = True
                    else:
                        free = False
            if event.type == pygame.MOUSEMOTION:
                if event.pos[1] < 47:
                    if event.pos[0] < 552:
                        check_left = True
                        check_right = False
                    else:
                        check_right = True
                        check_left = False
                else:
                    check_right = False
                    check_left = False
            back.update(event)
            if return_to_menu:
                return_to_menu = False
                return
        backgroung_menu_image.draw()
        font = pygame.font.Font("data/8693.ttf", 55)
        font2 = pygame.font.Font("data/8693.ttf", 60)
        if check_left:
            text = font2.render(str("Свободный режим"), 1, (255, 229, 0))
        else:
            text = font.render(str("Свободный режим"), 1, (255, 229, 0))
        screen.blit(text, (100, 0))
        if check_right:
            text = font2.render(str("Режим волн"), 1, (255, 229, 0))
        else:
            text = font.render(str("Режим волн"), 1, (255, 229, 0))
        screen.blit(text, (650, 0))
        back.draw()
        con = sqlite3.connect("data/record.db")
        cur = con.cursor()
        font = pygame.font.Font("data/8693.ttf", 40)
        y = 50
        x = 0
        text = font.render(str("Место"), 1, (255, 229, 0))
        screen.blit(text, (x, y))
        x += 150
        text = font.render(str("НИКНЕЙМ"), 1, (255, 229, 0))
        screen.blit(text, (x, y))
        x += 425
        text = font.render(str("ЛУЧШИЙ СЧЁТ"), 1, (255, 229, 0))
        screen.blit(text, (x, y))
        x += 225
        text = font.render(str("ПОСЛЕДНИЙ СЧЁТ"), 1, (255, 229, 0))
        screen.blit(text, (x, y))
        if free:
            y = 100
            result = sorted(cur.execute("""SELECT * FROM Free_mode""").fetchall(),
                            key=lambda x: int(-x[1]))
            for i in range(10 if len(result) > 10 else len(result)):
                x = 0
                text = font.render(str(f"{i + 1}"), 1, (255, 229, 0))
                screen.blit(text, (x, y))
                x += 150
                text = font.render(str(f"{result[i][0]}"), 1, (255, 229, 0))
                screen.blit(text, (x, y))
                x += 500
                text = font.render(str(f"{result[i][1]}"), 1, (255, 229, 0))
                screen.blit(text, (x, y))
                x += 300
                text = font.render(str(f"{result[i][2]}"), 1, (255, 229, 0))
                screen.blit(text, (x, y))
                y += 50
        else:
            y = 100
            result = cur.execute("""SELECT * FROM Wave_mode""").fetchall()
            for i in range(10 if len(result) > 10 else len(result)):
                x = 0
                text = font.render(str(f"{i + 1}"), 1, (255, 229, 0))
                screen.blit(text, (x, y))
                x += 150
                text = font.render(str(f"{result[i][0]}"), 1, (255, 229, 0))
                screen.blit(text, (x, y))
                x += 500
                text = font.render(str(f"{result[i][1]}"), 1, (255, 229, 0))
                screen.blit(text, (x, y))
                x += 300
                text = font.render(str(f"{result[i][2]}"), 1, (255, 229, 0))
                screen.blit(text, (x, y))
                y += 50
        con.commit()
        con.close()
        pygame.display.flip()
        clock.tick(10000)
    pygame.quit()


def draw_level(name_file, nicname):
    global MUSIC_check
    MUSIC_check = False
    MUSIC.stop()
    im = Image.open(f'data/{name_file}')
    pixels = im.load()
    x, y = im.size
    points = []
    road_sprites_horizontal = pygame.sprite.Group()
    road_sprites_vertical = pygame.sprite.Group()
    trees_sprite = pygame.sprite.Group()
    road_sprites_rotate = pygame.sprite.Group()
    evil_points = []
    tower_coords = []
    for i in range(x):
        for j in range(y):
            if pixels[i, j][0] == pixels[i, j][1] == pixels[i, j][2] == 0:
                points.append((i, j))
            elif pixels[i, j][0] == 255 and pixels[i, j][1] == pixels[i, j][
                2] == 0:
                points.insert(0, (i, j))
            elif pixels[i, j][0] == 255 and pixels[i, j][1] == 255 and \
                    pixels[i, j][2] == 0:
                tower_coords.append((i - 25, j - 25))
    C_end = (64, 440)
    points.append(C_end)
    k = len(points) - 1
    C = points[0]
    evil_points.append(C)

    for i in range(k):
        min_s = 0
        min_point = None
        x1, y1 = C
        for point in points:
            x2, y2 = point
            if x1 != x2 or y1 != y2:
                s = (x2 - x1) ** 2 + (y2 - y1) ** 2
                if s < min_s or min_s == 0:
                    min_s = s
                    min_point = point
        x2, y2 = min_point

        if x1 < x2 and y1 < y2:
            Road(road_sprites_horizontal, road_sprites_vertical, road_sprites_rotate, 'h', x1, y1,
                 x2, y2)
            Road(road_sprites_horizontal, road_sprites_vertical, road_sprites_rotate, 'v', x1, y1,
                 x2, y2, road='right')
            Road(road_sprites_horizontal, road_sprites_vertical, road_sprites_rotate, 'r', x2, y1,
                 rotate=270)
            Road(road_sprites_horizontal, road_sprites_vertical, road_sprites_rotate, 'r', x2, y2,
                 rotate=90)
            evil_points.append((x2 + X, y1 + Y, 0, V_E, 0))
            evil_points.append((x2 + X, y2 + Y, V_E, 0, 0))

        elif x2 < x1 and y2 > y1:
            Road(road_sprites_horizontal, road_sprites_vertical, road_sprites_rotate, 'h', x2, y2,
                 x1, y1)
            Road(road_sprites_horizontal, road_sprites_vertical, road_sprites_rotate, 'v', x1, y1,
                 x2, y2)
            Road(road_sprites_horizontal, road_sprites_vertical, road_sprites_rotate, 'r', x1, y2,
                 rotate=180)
            Road(road_sprites_horizontal, road_sprites_vertical, road_sprites_rotate, 'r', x1, y1,
                 rotate=0)
            evil_points.append((x1 + X, y1 + Y, 0, V_E, 0))
            evil_points.append((x1 + X, y2 + Y, - V_E, 0, 0))

        elif x1 < x2 and y1 > y2:
            Road(road_sprites_horizontal, road_sprites_vertical, road_sprites_rotate, 'h', x1, y1,
                 x2, y2)
            Road(road_sprites_horizontal, road_sprites_vertical, road_sprites_rotate, 'v', x2, y2,
                 x1, y1)
            Road(road_sprites_horizontal, road_sprites_vertical, road_sprites_rotate, 'r', x2, y1,
                 rotate=180)
            Road(road_sprites_horizontal, road_sprites_vertical, road_sprites_rotate, 'r', x2, y2,
                 rotate=0)
            evil_points.append((x2 + X, y1 + Y, 0, - V_E, 0))
            evil_points.append((x2 + X, y2 + Y, V_E, 0, 0))

        elif x2 < x1 and y2 < y1:
            Road(road_sprites_horizontal, road_sprites_vertical, road_sprites_rotate, 'h', x2, y2,
                 x1, y1)
            Road(road_sprites_horizontal, road_sprites_vertical, road_sprites_rotate, 'v', x2, y2,
                 x1, y1, road='right')
            Road(road_sprites_horizontal, road_sprites_vertical, road_sprites_rotate, 'r', x1, y2,
                 rotate=270)
            Road(road_sprites_horizontal, road_sprites_vertical, road_sprites_rotate, 'r', x2, y2,
                 rotate=90)
            evil_points.append((x1 + X, y2 + Y, - V_E, 0, 0))
            evil_points.append((x2 + X, y2 + Y, 0, - V_E, 0))

        if points:
            points.remove(C)
        C = min_point

    evil_points.append((C_end[0] + X, C_end[1] + Y, 0, 0, 0))
    evil_points.append((C_end[0] + 1 + X, C_end[1] + 1 + Y, 0, 0, 0))
    x1, y1 = evil_points[0]
    x2, y2 = evil_points[1][0], evil_points[1][1]
    if x1 <= x2 and y1 <= y2:
        evil_points[0] = (x1 + X, y1 + Y, V_E, 0, 0)
    elif x1 <= x2 and y1 >= y2:
        evil_points[0] = (x1 + X, y1 + Y, V_E, 0, 0)
    if x1 >= x2 and y1 <= y2:
        evil_points[0] = (x1 + X, y1 + Y, - V_E, 0, 0)
    if x1 >= x2 and y1 >= y2:
        evil_points[0] = (x1 + X, y1 + Y, 0, - V_E, 0)

    global V1, V2
    global check_pause
    global check_restart
    global check_exit
    towers = []
    evils = []
    tower_sprites_1 = pygame.sprite.Group()
    for i in range(len(tower_coords)):
        a = Tower_and_build(tower_sprites_1, tower_coords[i])
        towers.append(a)
    for i in range(20 // k):
        Tree(trees_sprite, road_sprites_horizontal, road_sprites_vertical, road_sprites_rotate,
             tower_sprites_1)
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
    MoveEvil2 = 26
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
    Pause(menu)
    Continue(menu_pause)
    Restart(menu_restart)
    Exit(menu_exit)
    a = Evil(Evil_sprites, True, evil_points)
    evils.append(a)
    a = Evil2(Evil2_sprites, True, evil_points)
    evils.append(a)
    pygame.time.set_timer(Cityanim, 1000)
    pygame.time.set_timer(Seaanim, 2000)
    pygame.time.set_timer(Electroanim, 100)
    pygame.time.set_timer(MoveEvil, 50)
    pygame.time.set_timer(AddEvil, V1)
    pygame.time.set_timer(AddEvil2, V2)
    pygame.time.set_timer(Buildanim, 1000)
    pygame.time.set_timer(Hit, 1000)
    pygame.time.set_timer(MoveGun, 5)
    pygame.time.set_timer(MoveEvil2, 50)
    running = True
    while running:
        if check_pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
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
            screen.blit(load_image("pause/fon_pause.png"), (0, 0))
            font = pygame.font.Font("data/8693.ttf", 50)
            text = font.render(str("Меню"), 1, (255, 229, 0))
            screen.blit(text, (500, 10))
            menu_pause.draw(screen)
            menu_exit.draw(screen)
            menu_restart.draw(screen)
        else:
            if check_restart or check_exit:
                V1, V2 = 20000, 10000
                pygame.time.set_timer(AddEvil, V1)
                pygame.time.set_timer(AddEvil2, V2)
                check_pause = False
                check_restart = False
                if check_exit:
                    check_exit = False
                    return
                towers = []
                evils = []
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
                a = Evil(Evil_sprites, True, evil_points)
                evils.append(a)
                a = Evil2(Evil2_sprites, True, evil_points)
                evils.append(a)
                gun_sprites = pygame.sprite.Group()
                tower_sprites_1 = pygame.sprite.Group()
                for i in range(len(tower_coords)):
                    a = Tower_and_build(tower_sprites_1, tower_coords[i])
                    towers.append(a)
                Pause(menu)
                Continue(menu_pause)
                Restart(menu_restart)
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
                    Evil_sprites.update(gun_sprites, Evil_sprites, player, AddEvil, AddEvil2)
                    for evil in Evil_sprites:
                        if (evil.rect.x, evil.rect.y) == (
                                evil_points[- 2][0], evil_points[-2][1]):
                            Evil_sprites.remove(evil)
                            player.heart -= 1
                            MINUSHEART.play()
                if event.type == MoveEvil2:
                    Evil2_sprites.update(gun_sprites, Evil2_sprites, player, AddEvil, AddEvil2)
                    for evil2 in Evil2_sprites:
                        if (evil2.rect.x == evil_points[-2][
                            0] or evil2.rect.x == evil_points[-1][0]) and (
                                evil2.rect.y == evil_points[-2][
                            1] or evil2.rect.y == evil_points[-1][1]):
                            Evil2_sprites.remove(evil2)
                            player.heart -= 1
                            MINUSHEART.play()
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
                        if not (runnin):
                            V1, V2 = 20000, 10000
                            pygame.time.set_timer(AddEvil, V1)
                            pygame.time.set_timer(AddEvil2, V2)
                            con = sqlite3.connect("data/record.db")
                            cur = con.cursor()
                            result = cur.execute("""SELECT player FROM Wave_mode""").fetchall()
                            if nicname not in [i[0] for i in result]:
                                cur.execute(f"""INSERT
                                               INTO
                                               Wave_mode(player, Best_Wave, Last_Wave)
                                               VALUES('{nicname}', {player.points}, {player.points})""")
                            else:
                                cur.execute(f"""UPDATE Wave_mode
                                                SET Last_Wave = {player.points}
                                                WHERE player = '{nicname}'""")
                                if player.points > int(cur.execute(
                                        f"""SELECT Best_Wave FROM Wave_mode WHERE player = '{nicname}'""").fetchone()[
                                                           0]):
                                    cur.execute(f"""UPDATE Wave_mode
                                                    SET Best_Wave = {player.points}
                                                    WHERE player = '{nicname}'""")
                            con.commit()
                            con.close()
                            return
                if event.type == AddEvil:
                    a = Evil(Evil_sprites, True, evil_points)
                    evils.append(a)
                if event.type == AddEvil2:
                    Evil2(Evil2_sprites, evil_points, evil_points)
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
            backgroung_image.draw(True)
            road_sprites_horizontal.draw(screen)
            road_sprites_vertical.draw(screen)
            road_sprites_rotate.draw(screen)
            cityo.draw()
            seao.draw()
            electroo.draw()
            Evil_sprites.draw(screen)
            Evil2_sprites.draw(screen)
            gun_sprites.draw(screen)
            trees_sprite.draw(screen)
            tower_sprites_1.draw(screen)
            menu.draw(screen)
            player.draw()
            tower_sprites_1.update()
        pygame.display.flip()
        clock.tick(10000)
    pygame.quit()


if __name__ == '__main__':
    name_menu = NameMenu()
    author_menu = AuthorMenu()
    name_levels = NameLevels()
    startmenu = StartMenu()
    endmenu = EndMenu()
    records = Records()
    backgroung_menu_image = BackgroundMenu()
    level1 = Level1()
    level2 = Level2()
    back = Back()

    while running_menu:
        if not (MUSIC_check):
            MUSIC.play()
            MUSIC_check = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_menu = False
            startmenu.update(event)
            endmenu.update(event)
            records.update(event)
        backgroung_menu_image.draw()
        name_menu.draw()
        author_menu.draw()
        startmenu.draw()
        endmenu.draw()
        records.draw()
        pygame.display.flip()
        clock.tick(10000)
    pygame.quit()
