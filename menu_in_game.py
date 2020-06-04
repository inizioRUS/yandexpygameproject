import pygame
from secondary_functions import *


class Game_over_anim:

    def __init__(self):
        super().__init__()
        self.pos = [-1080, 0]
        self.image = image = load_image('game_over_image.png')
        self.image = pygame.transform.scale(image, (1080, 720))

    def draw(self, screen):
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

    def draw(self, screen):
        screen.blit(self.image_heart, (50, -5))
        screen.blit(self.image_money, (200, 0))
        font = pygame.font.Font(None, 50)
        text = font.render(str(self.heart), 1, (255, 255, 255))
        screen.blit(text, (120, 10))
        text = font.render(str(self.money), 1, (255, 255, 255))
        screen.blit(text, (250, 10))


class Pause(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.transform.scale(load_image("menu_in_game/menu_pause.png"), (50, 50))
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
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.transform.scale(load_image("pause/continue.png"), (200, 50))
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

    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.transform.scale(load_image("pause/restart.png"), (200, 250))
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

    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.transform.scale(load_image("pause/exit.png", (255, 255, 255)), (200, 50))
        self.rect = self.image.get_rect()
        self.rect.x = 450
        self.rect.y = 575

    def get_click(self, pos):
        if self.rect.x <= pos[0] and self.rect.y <= pos[1] and self.rect.x + \
                self.rect.size[0] >= \
                pos[0] and self.rect.y + self.rect.size[1] >= pos[1]:
            return True
        return False
