import pygame
import os
from random import choice
from math import asin, pi, sqrt, sin, cos, atan

ROAD = [[[1080, 120, -5, 0, 0], [320, 120, 3, 5, 1], [500, 420, -4, 5, 1],
         [436, 500, -3, -1, 0],
         [49, 371, 0, 0, 0], [50, 372]],
        [[1080, 280, -5, 0, 0], [380, 280, 3, 4, 1], [500, 440, -4, 5, 1],
         [436, 520, -3, -1, 0],
         [49, 391, 0, 0, 0], [50, 392]]]
COOR_BUILD = [(250, 140), (360, 65), (500, 225), (800, 370), (575, 375),
              (250, 550), (220, 370),
              (310, 390)]
V = 500
pygame.init()
size = width, height = 1080, 720
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


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


class Player:
    def __init__(self):
        self.heart = 20
        self.money = 200
        self.image_heart = load_image('heart.png', (255, 255, 255))
        self.image_heart = pygame.transform.scale(self.image_heart, (90, 60))
        self.image_money = load_image('money.jpg', (255, 255, 255))
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
    image_1 = load_image('gun.png', (255, 255, 255))
    image_1 = pygame.transform.scale(image_1, (25, 25))
    image_2 = load_image('boom.jpg')
    image_2 = pygame.transform.scale(image_2, (50, 50))

    def __init__(self, group, *args):
        super().__init__(group)
        self.image = self.image_1
        self.rect = self.image.get_rect()
        self.rect.x = args[0]
        self.rect.y = args[1]
        self.boom = False
        self.i = 0
        self.dx = V // 100 * cos(args[2])
        self.dy = V // 100 * sin(args[2])

    def update(self):
        if self.boom:
            if self.i == 0:
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

    def get_click(self, pos):
        if self.rect.x <= pos[0] and self.rect.y <= pos[1] and self.rect.x + \
                self.rect.size[0] >= \
                pos[0] and self.rect.y + self.rect.size[1] >= pos[1] and not (
                self.built):
            if player.money >= 100:
                self.startbuild = True
                player.money -= 100

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

    def update(self):
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
            Evil_sprites.remove(self)
            player.money += 20


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
player = Player()
Evil_sprites = pygame.sprite.Group()
a = Evil(Evil_sprites)
evils.append(a)
gun_sprites = pygame.sprite.Group()
Hit = 29
MoveGun = 27
for i in range(8):
    a = Tower_and_build(tower_sprites_1, COOR_BUILD[i])
    towers.append(a)

if __name__ == '__main__':
    pygame.time.set_timer(Cityanim, 1000)
    pygame.time.set_timer(Seaanim, 2000)
    pygame.time.set_timer(Electroanim, 100)
    pygame.time.set_timer(MoveEvil, 200)
    pygame.time.set_timer(AddEvil, 20000)
    pygame.time.set_timer(Buildanim, 1000)
    pygame.time.set_timer(Hit, 2000)
    pygame.time.set_timer(MoveGun, 10)
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
            if event.type == MoveEvil:
                Evil_sprites.update()
                for evil in Evil_sprites:
                    if evil.rect.x == 49 and (
                            evil.rect.y == 371 or evil.rect.y == 391):
                        Evil_sprites.remove(evil)
                        player.heart -= 1
            if event.type == AddEvil:
                a = Evil(Evil_sprites)
                evils.append(a)
            if event.type == Buildanim:
                for i in towers:
                    i.builds()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i in towers:
                        i.get_click(event.pos)
            if event.type == pygame.MOUSEMOTION:
                for i in towers:
                    i.check_change(event.pos)
            if event.type == Hit:
                for build in tower_sprites_1:
                    if build.built:
                        x1, y1 = build.rect.x, build.rect.y
                        for evil in Evil_sprites:
                            x2, y2 = evil.rect.x, evil.rect.y
                            if (x2 - x1) ** 2 + (y2 - y1) ** 2 <= 40000:
                                angle = count_coords(x1 + 20, y1 + 20, x2 + 30,
                                                     y2 + 30)
                                if angle:
                                    Gun(gun_sprites, x1 + 20, y1 + 20, angle)
                                    break

            if event.type == MoveGun:
                gun_sprites.update()
        backgroung_image.draw()
        player.draw()
        cityo.draw()
        seao.draw()
        electroo.draw()
        Evil_sprites.draw(screen)
        tower_sprites_1.draw(screen)
        tower_sprites_1.update()
        gun_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(10000)
    pygame.quit()
