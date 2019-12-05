import pygame
import os
from random import choice

ROAD = [[[1000, 100, -5, 0], [470, 100]], [[1000, 250, -5, 0], [380, 250, 3, 4], [503, 410]]]
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


class Evil(pygame.sprite.Sprite):
    image = load_image('Evil/evil.png', (255, 255, 255))
    image2 = load_image('Evil/evil2.png', (255, 255, 255))
    image = pygame.transform.scale(image, (100, 100))
    image2 = pygame.transform.scale(image2, (100, 100))
    image = pygame.transform.flip(image, True, False)
    image2 = pygame.transform.flip(image2, True, False)

    def __init__(self, group):
        super().__init__(group)
        self.coords = ROAD[choice([1, 1])]
        self.pos = 0
        self.image = Evil.image
        self.rect = self.image2.get_rect()
        self.rect.x, self.rect.y, self.d_x, self.d_y = self.coords[self.pos]

    def update(self):
        self.image = Evil.image2 if self.image == Evil.image else Evil.image
        if self.rect.x <= self.coords[self.pos + 1][0] and self.rect.y >= \
                self.coords[self.pos + 1][1]:
            self.pos += 1
            self.rect.x, self.rect.y, self.d_x, self.d_y = self.coords[
                self.pos]
        self.rect.x += self.d_x
        self.rect.y += self.d_y


class Backgroung():
    def __init__(self):
        self.image = load_image("fonmain.png")
        self.image = pygame.transform.scale(self.image, (1080, 720))

    def draw(self):
        screen.blit(self.image, (0, 0))


class City():
    image = load_image("city/city1.png")
    image = pygame.transform.scale(image, (1080, 720))
    image2 = load_image("city/city2.png")
    image2 = pygame.transform.scale(image2, (1080, 720))
    image3 = load_image("city/city3.png")
    image3 = pygame.transform.scale(image3, (1080, 720))
    images = [image, image2, image3]

    def __init__(self):
        self.status = "U"
        self.statusi = 1
        self.image = City.images[self.statusi]
        screen.blit(self.image, (0, 0))

    def cheageimage(self):
        if self.status == "U":
            self.statusi += 1
            if self.statusi == 2:
                self.status = "D"
        else:
            self.statusi -= 1
            if self.statusi == 0:
                self.status = "U"
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
        self.status = "U"
        self.statusi = 1
        self.image = Sea.images[self.statusi]
        screen.blit(self.image, (0, 0))

    def cheageimage(self):
        if self.status == "U":
            self.statusi += 1
            if self.statusi == 2:
                self.status = "D"
        else:
            self.statusi -= 1
            if self.statusi == 0:
                self.status = "U"
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
        self.status = "U"
        self.statusi = 1
        self.image = Electro.images[self.statusi]
        screen.blit(self.image, (0, 0))

    def cheageimage(self):
        if self.status == "U":
            self.statusi += 1
            if self.statusi == 2:
                self.status = "D"
        else:
            self.statusi -= 1
            if self.statusi == 0:
                self.status = "U"
        self.image = Electro.images[self.statusi]

    def draw(self):
        screen.blit(self.image, (0, 0))


backgroung_image = Backgroung()
cityo = City()
electroo = Electro()
seao = Sea()
Cityanim = 1
Seaanim = 2
Electroanim = 3
MoveEvil = 30
all_sprites = pygame.sprite.Group()
Evil(all_sprites)


def main():
    pygame.time.set_timer(Cityanim, 1000)
    pygame.time.set_timer(Seaanim, 2000)
    pygame.time.set_timer(Electroanim, 100)
    pygame.time.set_timer(MoveEvil, 400)
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
                all_sprites.update()
        backgroung_image.draw()
        cityo.draw()
        seao.draw()
        electroo.draw()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(10000)
    pygame.quit()


main()
