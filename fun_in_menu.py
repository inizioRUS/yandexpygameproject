import sqlite3
import pygame
from secondary_functions import *


def levels(create_particles, level1, level2, name, back, Particle, backgroung_menu_image,
           screen, name_levels, screen_rect, clock, MUSIC_check, pre_Preview, input_file,
           draw_level, Image, X, Y, V_E, game, Backgroung, City, Electro, Sea, Tower_and_build,
           COOR_BUILD_PRE, Tree, size, Player, Pause, Continue, Restart, Exit, Evil, choice,
           Evil2,
           ROAD2, V1, V2, Game_over_anim, Gun, V, ROAD, sound):
    running_levels = True
    particles = pygame.sprite.Group()
    while running_levels:
        if not (MUSIC_check):
            sound["MUSIC"].play()
            MUSIC_check = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_levels = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                create_particles(pygame.mouse.get_pos(), particles, Particle)
            level1.update(name, pre_Preview, input_file, back, backgroung_menu_image, screen, clock,
                          draw_level, Image, X, Y, V_E, game, Backgroung, City, Electro, Sea,
                          Tower_and_build, COOR_BUILD_PRE, Tree, size,
                          Player, Pause, Continue, Restart, Exit, Evil, choice, Evil2,
                          ROAD2, V1, V2, Game_over_anim,
                          Gun, V, ROAD, sound, event)
            level2.update(name, pre_Preview, input_file, back, backgroung_menu_image, screen, clock,
                          draw_level, Image, X, Y, V_E, game, Backgroung, City, Electro, Sea,
                          Tower_and_build, COOR_BUILD_PRE, Tree, size,
                          Player, Pause, Continue, Restart, Exit, Evil, choice, Evil2,
                          ROAD2, V1, V2, Game_over_anim,
                          Gun,
                          V, ROAD, sound, event)
            if back.update(event):
                return False
        backgroung_menu_image.draw(screen)
        name_levels.draw(screen)
        level1.draw(screen)
        level2.draw(screen)
        particles.update(screen_rect)
        particles.draw(screen)
        back.draw(screen)
        pygame.display.flip()
        clock.tick(10000)
    pygame.quit()


def name(level, pre_Preview, input_file, back, backgroung_menu_image, screen, clock, draw_level,
         Image, X, Y, V_E, game, Backgroung, City, Electro, Sea, Tower_and_build,
         COOR_BUILD_PRE, Tree, size,
         Player, Pause, Continue, Restart, Exit, Evil, choice, Evil2,
         ROAD2, V1, V2, Game_over_anim, Gun,
         V, ROAD, sound):
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
                        pre_Preview(nicname, Backgroung, City, screen, Electro, Sea,
                                    Tower_and_build, COOR_BUILD_PRE, clock, game, Tree, size, Player,
                                    Pause, Continue, Restart, Exit, Evil, choice, Evil2,
                                    ROAD2, V1, V2, Game_over_anim,
                                    Gun, V, ROAD, sound)
                        return_to_menu = True
                    else:
                        input_file(nicname, draw_level, back, screen, backgroung_menu_image, clock,
                                   Image, X, Y,
                                   V_E, game, Tower_and_build, Tree,
                                   size, Backgroung, City, Electro, Sea, Player, Pause,
                                   Continue, Restart, Exit, Evil, choice, Evil2, ROAD2, V1,
                                   V2,
                                   Game_over_anim, Gun, V,
                                   ROAD, sound)
                        return_to_menu = True
                elif keys[pygame.K_BACKSPACE]:
                    nicname = nicname[:-1]
                elif len(nicname) < 25:
                    nicname += event.unicode
            if back.update(event):
                return False
        backgroung_menu_image.draw(screen)
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
        back.draw(screen)
        pygame.display.flip()
        clock.tick(10000)
    pygame.quit()


def input_file(nicname, draw_level, back, screen, backgroung_menu_image, clock, Image, X, Y,
               V_E, game, Tower_and_build, Tree,
               size, Backgroung, City, Electro, Sea, Player, Pause,
               Continue, Restart, Exit, Evil, choice, Evil2, ROAD2, V1, V2,
               Game_over_anim,  Gun, V,
               ROAD, sound):
    file = ''
    running_levels = True
    while running_levels:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_levels = False
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[13]:
                    draw_level(file, nicname, Image, X, Y, V_E, game, Tower_and_build, Tree,
                               size, Backgroung, City, screen, Electro, Sea, Player, Pause,
                               Continue, Restart, Exit, Evil, choice, Evil2, ROAD2, V1, V2,
                               Game_over_anim, clock,  Gun, V,
                               ROAD, sound)
                    return_to_menu = True
                elif keys[pygame.K_BACKSPACE]:
                    file = file[:-1]
                elif len(file) < 25:
                    file += event.unicode
            if back.update(event):
                return
        backgroung_menu_image.draw(screen)
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
        back.draw(screen)
        pygame.display.flip()
        clock.tick(10000)
    pygame.quit()


def record(back, Particle, screen, backgroung_menu_image, screen_rect, clock):
    free = True
    check_right = False
    check_left = False
    running_levels = True
    particles = pygame.sprite.Group()
    while running_levels:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_levels = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                create_particles(pygame.mouse.get_pos(), particles, Particle)
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
            if back.update(event):
                return False
        backgroung_menu_image.draw(screen)
        particles.update(screen_rect)
        particles.draw(screen)
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
        back.draw(screen)
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


def pre_Preview(nicname, Backgroung, City, screen, Electro, Sea, Tower_and_build,
                COOR_BUILD_PRE, clock, game, Tree, size, Player,
                Pause, Continue, Restart, Exit, Evil, choice, Evil2,
                ROAD2, V1, V2, Game_over_anim, Gun, V, ROAD, sound):
    sound["MUSIC"].stop()
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
    cityo = City(screen, False)
    electroo = Electro(screen, False)
    seao = Sea(screen, False)
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
                    game(nicname, Tower_and_build, Tree, size, Backgroung, City, screen, Electro,
                         Sea, Player, Pause,
                         Continue, Restart, Exit, Evil, ROAD, choice, Evil2, ROAD2, V1, V2,
                         Game_over_anim, clock, Gun, V, sound)
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
        backgroung_image.draw(screen)
        cityo.draw(screen)
        seao.draw(screen)
        electroo.draw(screen)
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
