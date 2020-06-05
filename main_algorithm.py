import sqlite3
from secondary_functions import *


def game(nicname, Tower_and_build, Tree, size, Backgroung, City, screen, Electro, Sea, Player, Pause,
         Continue, Restart, Exit, Evil, ROAD, choice, Evil2, ROAD2, V1, V2,
         Game_over_anim, clock, Gun, V, sound,
         tower_coords=[(250, 140), (360, 65), (500, 225), (800, 370), (575, 375),
                       (250, 550), (220, 370),
                       (310, 390)], k=1, trees_sprite=[], road_sprites_horizontal=[],
         road_sprites_vertical=[],
         road_sprites_rotate=[], evil_points=[], check_game_view=False):
    towers = []
    evils = []
    print(tower_coords)
    check_pause = False
    check_restart = False
    check_exit = False
    tower_sprites_1 = pygame.sprite.Group()
    if check_game_view:
        for i in range(len(tower_coords)):
            a = Tower_and_build(tower_sprites_1, tower_coords[i])
            towers.append(a)
        for i in range(20 // k):
            Tree(trees_sprite, road_sprites_horizontal, road_sprites_vertical, road_sprites_rotate,
                 tower_sprites_1, size)
    else:
        for i in range(len(tower_coords)):
            a = Tower_and_build(tower_sprites_1, tower_coords[i])
            towers.append(a)
    backgroung_image = Backgroung()
    cityo = City(screen)
    electroo = Electro(screen)
    seao = Sea(screen)
    Cityanim = 1
    Seaanim = 2
    Electroanim = 3
    Buildanim = 10
    MoveEvil = 30
    MoveEvil2 = 26
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

    Pause(menu)
    Continue(menu_pause)
    Restart(menu_restart)
    Exit(menu_exit)
    a = Evil(Evil_sprites, check_game_view, ROAD, choice, sound['ZOMBI'], evil_points)
    evils.append(a)
    a = Evil2(Evil2_sprites, check_game_view, ROAD2, choice, evil_points)
    evils.append(a)
    pygame.time.set_timer(Cityanim, 1000)
    pygame.time.set_timer(Seaanim, 2000)
    pygame.time.set_timer(Electroanim, 100)
    pygame.time.set_timer(MoveEvil, 50 if check_game_view else 100)
    pygame.time.set_timer(MoveEvil2, 50 if check_game_view else 100)
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
                cityo = City(screen)
                electroo = Electro(screen)
                seao = Sea(screen)
                player = Player()
                Evil_sprites = pygame.sprite.Group()
                Evil2_sprites = pygame.sprite.Group()
                menu = pygame.sprite.Group()
                menu_pause = pygame.sprite.Group()
                menu_restart = pygame.sprite.Group()
                a = Evil(Evil_sprites, check_game_view, ROAD, choice, sound['ZOMBI'], evil_points)
                evils.append(a)
                a = Evil2(Evil2_sprites, check_game_view, ROAD2, choice, evil_points)
                evils.append(a)
                gun_sprites = pygame.sprite.Group()
                print(tower_sprites_1)
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
                if check_game_view:
                    if event.type == MoveEvil:
                        Evil_sprites.update(gun_sprites, Evil_sprites, player, AddEvil, AddEvil2, V1,
                                            V2,
                                            sound['MONEY'])
                        for evil in Evil_sprites:
                            if (evil.rect.x, evil.rect.y) == (
                                    evil_points[- 2][0], evil_points[-2][1]):
                                Evil_sprites.remove(evil)
                                player.heart -= 1
                                sound['MINUSHEART'].play()
                    if event.type == MoveEvil2:
                        Evil2_sprites.update(gun_sprites, Evil2_sprites, player, AddEvil, AddEvil2,
                                             V1,
                                             V2, sound['MONEY'])
                        for evil2 in Evil2_sprites:
                            if (evil2.rect.x == evil_points[-2][
                                0] or evil2.rect.x == evil_points[-1][0]) and (
                                    evil2.rect.y == evil_points[-2][
                                1] or evil2.rect.y == evil_points[-1][1]):
                                Evil2_sprites.remove(evil2)
                                player.heart -= 1
                                sound['MINUSHEART'].play()
                else:
                    if event.type == MoveEvil:
                        Evil_sprites.update(gun_sprites, Evil_sprites, player, AddEvil, AddEvil2, V1,
                                            V2,
                                            sound['MONEY'])
                        for evil in Evil_sprites:
                            if evil.rect.x == 49 and (
                                    evil.rect.y == 371 or evil.rect.y == 391):
                                Evil_sprites.remove(evil)
                                sound['MINUSHEART'].play()
                                player.heart -= 1
                        Evil2_sprites.update(gun_sprites, Evil2_sprites, player, AddEvil, AddEvil2,
                                             V1,
                                             V2, sound['MONEY'])
                        for evil2 in Evil2_sprites:
                            if evil2.rect.x == 52 and (
                                    evil2.rect.y == 372 or evil2.rect.y == 392):
                                Evil2_sprites.remove(evil2)
                                sound['MINUSHEART'].play()
                                player.heart -= 1
                if player.heart < 1:
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
                    runnin = True
                    game_over = Game_over_anim()
                    while runnin:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                runnin = False
                        clock.tick(200)
                        game_over.draw(screen)
                        pygame.display.flip()
                        if not game_over.update():
                            return
                if event.type == AddEvil:
                    a = Evil(Evil_sprites, check_game_view, ROAD, choice, sound['ZOMBI'], evil_points)
                    evils.append(a)
                if event.type == AddEvil2:
                    a = Evil2(Evil2_sprites, check_game_view, ROAD2, choice, evil_points)
                    evils.append(a)
                if event.type == Buildanim:
                    for i in towers:
                        i.builds(sound['BUILDED'])
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for i in towers:
                            i.get_click(event.pos, player, sound['BUILD'], sound['NEEDDOLD'])
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
                                if (x2 + 30 - x1 - 20) ** 2 + (y2 + 30 - y1 - 20) ** 2 <= 30000:
                                    angle = count_coords(x1 + 20, y1 + 20,
                                                         x2 + 30,
                                                         y2 + 30)
                                    if angle:
                                        Gun(gun_sprites, sound['BUL'], V, x1 + 20, y1 + 20,
                                            angle)
                                        hit_done = True
                                        print(1)
                                        break
                            if not hit_done:
                                for evil2 in Evil2_sprites:
                                    x2, y2 = evil2.rect.x, evil2.rect.y
                                    if (x2 + 30 - x1 - 20) ** 2 + (
                                            y2 + 30 - y1 - 20) ** 2 <= 30000:
                                        angle = count_coords(x1 + 20, y1 + 20,
                                                             x2 + 30,
                                                             y2 + 30)
                                        if angle:
                                            Gun(gun_sprites, sound['BUL'], V, x1 + 20, y1 + 20,
                                                angle)
                                            print(2)
                                            break

                if event.type == MoveGun:
                    gun_sprites.update(gun_sprites, sound['BOOM'])
            backgroung_image.draw(screen, True if check_game_view else False)
            if check_game_view:
                road_sprites_horizontal.draw(screen)
                road_sprites_vertical.draw(screen)
                road_sprites_rotate.draw(screen)
            player.draw(screen)
            cityo.draw(screen)
            seao.draw(screen)
            electroo.draw(screen)
            Evil_sprites.draw(screen)
            Evil2_sprites.draw(screen)
            gun_sprites.draw(screen)
            if check_game_view:
                trees_sprite.draw(screen)
            tower_sprites_1.draw(screen)
            menu.draw(screen)
            tower_sprites_1.update()
        pygame.display.flip()
        clock.tick(10000)
    pygame.quit()
