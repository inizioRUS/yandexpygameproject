import pygame
from secondary_functions import *


class Road(pygame.sprite.Sprite):

    def __init__(self, group1, group2, group3, mod, x1, y1, x2=0, y2=0, rotate=0, road='left'):
        if mod == 'h':
            super().__init__(group1)
            self.image = load_image('create_road/stright_.png', (255, 255, 255))
            self.rect = self.image.get_rect()
            self.image = pygame.transform.scale(self.image,
                                                (x2 - x1, self.rect.h))
            self.rect.x = x1
            self.rect.y = y1 - self.rect.h // 2
        elif mod == 'v':
            super().__init__(group2)
            self.image = pygame.transform.rotate(
                load_image('create_road/stright_.png', (255, 255, 255)), 90)
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
            self.image = load_image('create_road/rotate_new.png', (255, 255, 255))
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

    def __init__(self, group, road_sprites_horizontal, road_sprites_rotate, road_sprites_vertical,
                 tower_sprites_1, size):
        super().__init__(group)
        self.image = pygame.transform.scale(load_image('trees.png', (255, 255, 255)), (75, 150))
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


def draw_level(name_file, nicname, Image, X, Y, V_E, game, Tower_and_build, Tree, size,
               Backgroung, City, screen, Electro, Sea, Player, Pause,
               Continue, Restart, Exit, Evil, choice, Evil2, ROAD2, V1, V2,
               Game_over_anim, clock, Gun, V, ROAD, sound):
    sound['MUSIC'].stop()
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
    game(nicname, Tower_and_build, Tree, size, Backgroung, City, screen, Electro, Sea, Player, Pause,
         Continue, Restart, Exit, Evil, ROAD, choice, Evil2, ROAD2, V1, V2,
         Game_over_anim, clock, Gun, V, sound, tower_coords, k,
         trees_sprite, road_sprites_horizontal,
         road_sprites_vertical,
         road_sprites_rotate, evil_points, True)
    return False
