from PIL import Image
from menu_objects import *
from menu_in_game import *
from entities_in_the_game import *
from objects_and_fun_to_generate import *
from fun_in_menu import *
from main_algorithm import *
from random import choice

pygame.mixer.init()  # иницилизация игры
pygame.init()  # иницилизация игры
sound = {'BUILDED': pygame.mixer.Sound('data/sound/builded.wav'),
         "BOOM": pygame.mixer.Sound('data/sound/boom.wav'),
         "BUL": pygame.mixer.Sound('data/sound/bul.wav'),
         "NEEDDOLD": pygame.mixer.Sound('data/sound/neeggold.wav'),
         "MONEY": pygame.mixer.Sound('data/sound/money.wav'),
         "ZOMBI": pygame.mixer.Sound('data/sound/zomb.wav'),
         "BUILD": pygame.mixer.Sound('data/sound/build.wav'),
         "MINUSHEART": pygame.mixer.Sound('data/sound/minusheart.wav'),
         "MUSIC": pygame.mixer.Sound('data/sound/music.wav')}  # флаг для включения и выключения музыки в меню
ROAD = [[[1080, 120, -5, 0, 0], [320, 120, 3, 5, 1], [500, 420, -4, 5, 1],
         [436, 500, -3, -1, 0],
         [49, 371, 0, 0, 0], [50, 372]],
        [[1080, 280, -5, 0, 0], [380, 280, 3, 4, 1], [500, 440, -4, 5, 1],
         [436, 520, -3, -1, 0],
         [49, 391, 0, 0, 0], [50, 392]]]  # константа дорог на карте для зомби
ROAD2 = [[[1080, 120, -10, 0, 0], [320, 120, 6, 10, 1], [500, 420, -8, 10, 1],
          [436, 500, -6, -2, 0],
          [52, 372, 0, 0, 0], [50, 372]],
         [[1080, 280, -10, 0, 0], [380, 280, 6, 8, 1], [500, 440, -8, 10, 1],
          [436, 520, -6, -2, 0],
          [52, 392, 0, 0, 0], [53, 393]]]  # константа дорог на карте для собак
COOR_BUILD_PRE = [(500, 280), (720, 130), (1000, 450), (1600, 740), (1150, 750),
                  (500, 1100), (440, 740),
                  (620, 780)]  # константа для башен на предпоказе карты
V1 = 20000  #
V2 = 10000  #
V = 500  #
V_E = 1  #
Y = - 60  #
X = - 45  #
size = width, height = 1080, 720
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
running_menu = True
screen_rect = (0, 0, width, height)

if __name__ == '__main__':
    MUSIC_check = False
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
    particles = pygame.sprite.Group()
    while running_menu:
        if not (MUSIC_check):
            sound["MUSIC"].play()
            MUSIC_check = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_menu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                create_particles(pygame.mouse.get_pos(), particles, Particle)
            startmenu.update(levels, create_particles, level1, level2, name, back, Particle,
                             backgroung_menu_image,
                             screen, name_levels, screen_rect, clock, MUSIC_check, pre_Preview,
                             input_file,
                             draw_level, Image, X, Y, V_E, game, Backgroung, City, Electro, Sea,
                             Tower_and_build,
                             COOR_BUILD_PRE, Tree, size,
                             Player, Pause, Continue, Restart, Exit, Evil, choice,Evil2,
                             ROAD2, V1, V2, Game_over_anim,
                             Gun, V, ROAD, sound, event)
            endmenu.update(event)
            records.update(record, back, Particle, screen, backgroung_menu_image, screen_rect, clock,
                           event)
        particles.update(screen_rect)
        backgroung_menu_image.draw(screen)
        particles.draw(screen)
        name_menu.draw(screen)
        author_menu.draw(screen)
        startmenu.draw(screen)
        endmenu.draw(screen)
        records.draw(screen)
        pygame.display.flip()
        clock.tick(10000)
    pygame.quit()
