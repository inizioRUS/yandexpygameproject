import pygame
import os
from random import choice

ROAD = [[[1080, 110, -5, 0, 0], [320, 110, 3, 5, 1], [500, 410, -4, 5, 1], [436, 490, -3, -1, 0],
         [49, 361, 0, 0, 0], [50, 362]],
        [[1080, 250, -5, 0, 0], [380, 250, 3, 4, 1], [500, 410, -4, 5, 1], [436, 490, -3, -1, 0],
         [49, 361, 0, 0, 0], [50, 362]]]
COOR_BUILD = [(250, 80), (430, 20), (500, 220), (650, 215), (575, 375), (250, 550), (220, 370),
              (310, 390)]
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


class Tower_and_build(pygame.sprite.Sprite):
    image = load_image("tower_and_build/tower_and_build1.png")
    image = pygame.transform.scale(image, (75, 75))
    image2 = load_image("tower_and_build/tower_and_build2.png")
    image2 = pygame.transform.scale(image2, (75, 75))
    image3 = load_image("tower_and_build/tower_and_build3.png")
    image3 = pygame.transform.scale(image3, (75, 75))
    image4 = load_image("tower_and_build/towerkiano.png")
    image4 = pygame.transform.scale(image4, (75, 125))
    images = [image, image2, image3, image4]

    def __init__(self, group, pos):
        super().__init__(group)
        self.checkcount = 0
        self.startbuild = False
        self.built = False
        self.status = "UP"
        self.statusi = 0
        self.image = Tower_and_build.images[self.statusi]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def get_click(self, pos):
        if self.rect.x <= pos[0] and self.rect.y <= pos[1] and self.rect.x + self.rect.size[0] >= \
                pos[0] and self.rect.y + self.rect.size[1] >= pos[1] and not (self.built):
            self.startbuild = True

    def update(self):
        if self.startbuild:
            print(self.checkcount)
            if self.checkcount == 4:
                self.built = True
                self.image = self.images[3]
                self.startbuild = False
                self.rect.x -= 0
                self.rect.y -= 50
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
                self.image = self.images[self.statusi]


class Evil(pygame.sprite.Sprite):
    image = load_image('Evil/evil.png', (255, 255, 255))
    image2 = load_image('Evil/evil2.png', (255, 255, 255))
    image = pygame.transform.scale(image, (100, 100))
    image2 = pygame.transform.scale(image2, (100, 100))
    image = pygame.transform.flip(image, True, False)
    image2 = pygame.transform.flip(image2, True, False)

    def __init__(self, group):
        super().__init__(group)
        self.coords = ROAD[choice([0, 1])]
        self.pos = 0
        self.image1 = Evil.image
        self.image2 = Evil.image2
        self.image = self.image1
        self.rect = self.image2.get_rect()
        self.rect.x, self.rect.y, self.d_x, self.d_y, flip = self.coords[self.pos]

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
tower_sprites = pygame.sprite.Group()
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
Evil_sprites = pygame.sprite.Group()
Evil(Evil_sprites)
for i in range(8):
    a = Tower_and_build(tower_sprites, COOR_BUILD[i])
    towers.append(a)


def main():
    pygame.time.set_timer(Cityanim, 1000)
    pygame.time.set_timer(Seaanim, 2000)
    pygame.time.set_timer(Electroanim, 100)
    pygame.time.set_timer(MoveEvil, 100)
    pygame.time.set_timer(AddEvil, 2500)
    pygame.time.set_timer(Buildanim, 2000)
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
                    if evil.rect.x == 49 and evil.rect.y == 361:
                        Evil_sprites.remove(evil)
            if event.type == AddEvil:
                Evil(Evil_sprites)
            if event.type == Buildanim:
                tower_sprites.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i in towers:
                        i.get_click(event.pos)
        backgroung_image.draw()
        cityo.draw()
        seao.draw()
        electroo.draw()
        tower_sprites.draw(screen)
        Evil_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(10000)
    pygame.quit()


main()
