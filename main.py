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


class Backgroung():
    def __init__(self):
        self.image = load_image("fon.jpg")
        self.image = pygame.transform.scale(self.image, (1080, 720))
        screen.blit(self.image, (0, 0))


class Evil(pygame.sprite.Sprite):
    image = load_image('evil.jpg', (255, 255, 255))
    image = pygame.transform.scale(image, (100, 100))

    def __init__(self, group):
        super().__init__(group)
        self.coords = ROAD[choice([1, 1])]
        self.pos = 0
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y, self.d_x, self.d_y = self.coords[self.pos]

    def update(self):
        if self.rect.x <= self.coords[self.pos + 1][0] and self.rect.y >= \
                self.coords[self.pos + 1][1]:
            self.pos += 1
            self.rect.x, self.rect.y, self.d_x, self.d_y = self.coords[
                self.pos]
        self.rect.x += self.d_x
        self.rect.y += self.d_y



def main():
    running = True
    Backgroung()
    all_sprites = pygame.sprite.Group()
    Evil(all_sprites)
    all_sprites.draw(screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
        Backgroung()
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(10000)
    pygame.quit()


main()
