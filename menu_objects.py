import pygame
import random
from secondary_functions import *
import sys


class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, dx, dy, particles):
        super().__init__(particles)
        self.image = pygame.transform.scale(
            random.choice([load_image("nuol.png"), load_image("one.png")]), (20, 20))
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

        self.gravity = 1

    def update(self, screen_rect):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


class BackgroundMenu:
    def __init__(self):
        self.image = load_image("menu/fonmenu.png")
        self.image = pygame.transform.scale(self.image, (1080, 720))

    def draw(self, screen):
        screen.blit(self.image, (0, 0))


class AuthorMenu:
    def __init__(self):
        self.image = load_image("menu/text5.png", (255, 255, 255))
        self.image = pygame.transform.scale(self.image, (108, 72))

    def draw(self, screen):
        screen.blit(self.image, (972, 670))


class NameMenu:
    def __init__(self):
        self.image = load_image("menu/name.png", (255, 255, 255))
        self.image = pygame.transform.scale(self.image, (1080, 720))

    def draw(self, screen):
        screen.blit(self.image, (30, 0))


class NameLevels:
    def __init__(self):
        self.image = load_image("menu/levels.png", (255, 255, 255))
        self.image = pygame.transform.scale(self.image, (540, 360))

    def draw(self, screen):
        screen.blit(self.image, (250, -120))


class StartMenu:
    image_start = load_image('menu/text1.png', (255, 255, 255))
    image_start = pygame.transform.scale(image_start, (300, 150))

    def __init__(self):
        self.check_size = False
        self.image = StartMenu.image_start
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 400

    def update(self, levels, create_particles, level1, level2, name, back, Particle,
               backgroung_menu_image,
               screen, name_levels, screen_rect, clock, MUSIC_check, pre_Preview, input_file,
               draw_level, Image, X, Y, V_E, game, Backgroung, City, Electro, Sea, Tower_and_build,
               COOR_BUILD_PRE, Tree, size,
               Player, Pause, Continue, Restart, Exit, Evil, choice, Evil2,
               ROAD2, V1, V2, Game_over_anim,
               Gun, V, ROAD, sound, *args

               ):

        if args and args[
            0].type == pygame.MOUSEMOTION and self.rect.collidepoint(
            args[0].pos):
            self.check_size = True
        elif args and args[
            0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(
            args[0].pos):
            levels(create_particles, level1, level2, name, back, Particle, backgroung_menu_image,
                   screen, name_levels, screen_rect, clock, MUSIC_check, pre_Preview, input_file,
                   draw_level, Image, X, Y, V_E, game, Backgroung, City, Electro, Sea,
                   Tower_and_build,
                   COOR_BUILD_PRE, Tree, size, Player, Pause, Continue, Restart, Exit, Evil, choice,
                   Evil2,
                   ROAD2, V1, V2, Game_over_anim, Gun, V, ROAD, sound)
        elif args and args[
            0].type == pygame.MOUSEMOTION and not (self.rect.collidepoint(
            args[0].pos)):
            self.check_size = False

    def draw(self, screen):
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

    def draw(self, screen):
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

    def update(self, record, back, Particle, screen, backgroung_menu_image, screen_rect, clock,
               *args):
        if args and args[
            0].type == pygame.MOUSEMOTION and self.rect.collidepoint(
            args[0].pos):
            self.check_size = True
        elif args and args[
            0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(
            args[0].pos):
            record(back, Particle, screen, backgroung_menu_image, screen_rect, clock)
        elif args and args[
            0].type == pygame.MOUSEMOTION and not (self.rect.collidepoint(
            args[0].pos)):
            self.check_size = False

    def draw(self, screen):
        if self.check_size:
            screen.blit(pygame.transform.scale(Records.image_records,
                                               (400, 200)), (self.rect.x, self.rect.y))
        else:
            screen.blit(pygame.transform.scale(Records.image_records,
                                               (300, 150)), (self.rect.x, self.rect.y))


class Level1:
    image_level_1 = load_image('menu/level1.png', (255, 255, 255))
    image_level_1 = pygame.transform.scale(image_level_1, (300, 150))

    def __init__(self):
        self.check_size = False
        self.image = Level1.image_level_1
        self.rect = self.image.get_rect()
        self.rect.x = 150
        self.rect.y = 300

    def update(self, name, pre_Preview, input_file, back, backgroung_menu_image, screen, clock
               , draw_level, Image, X, Y, V_E, game, Backgroung, City, Electro, Sea,
               Tower_and_build, COOR_BUILD_PRE, Tree, size, Player, Pause, Continue, Restart, Exit,
               Evil, choice, Evil2,
               ROAD2, V1, V2, Game_over_anim,
               Gun, V, ROAD, sound, *args):
        if args and args[
            0].type == pygame.MOUSEMOTION and self.rect.collidepoint(
            args[0].pos):
            self.check_size = True
        elif args and args[
            0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(
            args[0].pos):
            name(1, pre_Preview, input_file, back, backgroung_menu_image, screen, clock, draw_level,
                 Image, X, Y, V_E, game, Backgroung, City, Electro, Sea, Tower_and_build,
                 COOR_BUILD_PRE, Tree, size,
                 Player, Pause, Continue, Restart, Exit, Evil, choice, Evil2,
                 ROAD2, V1, V2, Game_over_anim, Gun,
                 V, ROAD, sound)
        elif args and args[
            0].type == pygame.MOUSEMOTION and not (self.rect.collidepoint(
            args[0].pos)):
            self.check_size = False

    def draw(self, screen):
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
        if args and args[
            0].type == pygame.MOUSEMOTION and self.rect.collidepoint(
            args[0].pos):
            self.check_size = True
        elif args and args[
            0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(
            args[0].pos):
            return True
        elif args and args[
            0].type == pygame.MOUSEMOTION and not (self.rect.collidepoint(
            args[0].pos)):
            self.check_size = False
        return False

    def draw(self, screen):
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

    def update(self, name, pre_Preview, input_file, back, backgroung_menu_image, screen, clock,
               draw_level, Image, X, Y, V_E, game, Backgroung, City, Electro, Sea,
               Tower_and_build, COOR_BUILD_PRE, Tree, size,
               Player, Pause, Continue, Restart, Exit, Evil, choice, Evil2,
               ROAD2, V1, V2, Game_over_anim, Gun,
               V, ROAD, sound,
               *args):
        if args and args[
            0].type == pygame.MOUSEMOTION and self.rect.collidepoint(
            args[0].pos):
            self.check_size = True
        elif args and args[
            0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(
            args[0].pos):
            name(2, pre_Preview, input_file, back, backgroung_menu_image, screen, clock, draw_level,
                 Image, X, Y, V_E, game, Backgroung, City, Electro, Sea, Tower_and_build,
                 COOR_BUILD_PRE, Tree, size,
                 Player, Pause, Continue, Restart, Exit, Evil, choice, Evil2,
                 ROAD2, V1, V2, Game_over_anim, Gun,
                 V, ROAD, sound)
        elif args and args[
            0].type == pygame.MOUSEMOTION and not (self.rect.collidepoint(
            args[0].pos)):
            self.check_size = False

    def draw(self, screen):
        if self.check_size:
            screen.blit(pygame.transform.scale(Level2.image_level_2,
                                               (400, 200)), (self.rect.x, self.rect.y))
        else:
            screen.blit(pygame.transform.scale(Level2.image_level_2,
                                               (300, 150)), (self.rect.x, self.rect.y))
