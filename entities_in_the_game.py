from secondary_functions import *


class Gun(pygame.sprite.Sprite):
    def __init__(self, group, BUL, V, *args):
        BUL.play()
        super().__init__(group)
        self.image = pygame.transform.scale(load_image('gun_and_boom/gun.png', (255, 255, 255)),
                                            (25, 25))
        self.rect = self.image.get_rect()
        self.rect.x = args[0]
        self.rect.y = args[1]
        self.boom = False
        self.i = 0
        self.dx = V // 100 * cos(args[2])
        self.dy = V // 100 * sin(args[2])

    def update(self, gun_sprites, BOOM):
        if self.boom:
            if self.i == 0:
                BOOM.play()
                self.image = pygame.transform.scale(load_image('gun_and_boom/boom.png'), (50, 50))
            self.i += 1
            if self.i == 50:
                gun_sprites.remove(self)
        else:
            self.rect.x += self.dx
            self.rect.y += self.dy


class Tower_and_build(pygame.sprite.Sprite):

    def __init__(self, group, pos, flag=True):
        super().__init__(group)
        if flag:
            self.images = [
                pygame.transform.scale(load_image("tower_and_build/tower_and_build1.png"), (50, 50)),
                pygame.transform.scale(load_image("tower_and_build/tower_and_build2.png"), (50, 50)),
                pygame.transform.scale(load_image("tower_and_build/tower_and_build3.png"), (50, 50)),
                pygame.transform.scale(
                    load_image("tower_and_build/tower_and_build1_move.png"),
                    (50, 50)),
                pygame.transform.scale(
                    load_image("tower_and_build/tower_and_build2_move.png"),
                    (50, 50)),
                pygame.transform.scale(
                    load_image("tower_and_build/tower_and_build3_move.png"),
                    (50, 50)),
                pygame.transform.scale(
                    load_image("tower_and_build/towerkiano.png"), (75, 150))]
            self.checkcount = 0
            self.change = False
            self.startbuild = False
            self.built = False
            self.status = "UP"
            self.statusi = 0
            self.image = self.images[self.statusi]
            self.rect = self.image.get_rect()
            self.rect.x = pos[0]
            self.rect.y = pos[1]
        else:
            self.image = pygame.transform.scale(load_image("tower_and_build/tower_and_build1.png"),
                                                (100, 100))
            self.rect = self.image.get_rect()
            self.rect.x = pos[0]
            self.rect.y = pos[1]

    def get_click(self, pos, player, BUILD, NEEDDOLD):
        if self.rect.x <= pos[0] and self.rect.y <= pos[1] and self.rect.x + \
                self.rect.size[0] >= \
                pos[0] and self.rect.y + self.rect.size[1] >= pos[1] and not (
                self.built):
            if player.money >= 100 and not (self.startbuild):
                self.startbuild = True
                BUILD.play()
                player.money -= 100
            elif self.startbuild:
                pass
            else:
                NEEDDOLD.play()

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

    def builds(self, BUILDED):
        if self.startbuild:
            if self.checkcount == 4:
                self.built = True
                self.change = False
                self.startbuild = False
                self.rect.x -= 0
                self.rect.y -= 70
                BUILDED.play()
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

    def __init__(self, group, check, ROAD, choice, ZOMBI, args):
        super().__init__(group)
        if check:
            self.coords = args
        else:
            self.coords = ROAD[choice([0, 1])]
        self.pos = 0
        self.hp = 70
        self.image1 = Evil.image
        self.image2 = Evil.image2
        self.image = self.image1
        self.rect = self.image2.get_rect()
        self.rect.x, self.rect.y, self.d_x, self.d_y, flip = self.coords[
            self.pos]
        ZOMBI.play()

    def update(self, gun_sprites, Evil_sprites, player, event1, event2, V1, V2, MONEY):
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
            MONEY.play()
            Evil_sprites.remove(self)
            player.money += 20
            player.points += 1
            if player.points % 10 == 0:
                V1 = V1 // 2
                V2 = V2 // 2
                pygame.time.set_timer(event1, V1)
                pygame.time.set_timer(event2, V2)


class Evil2(pygame.sprite.Sprite):
    image = load_image('Evil2/evil.png', (255, 255, 255))
    image2 = load_image('Evil2/evil2.png', (255, 255, 255))
    image = pygame.transform.scale(image, (105, 70))
    image2 = pygame.transform.scale(image2, (105, 70))
    image = pygame.transform.flip(image, True, False)
    image2 = pygame.transform.flip(image2, True, False)

    def __init__(self, group, check, ROAD2, choice, args):
        super().__init__(group)
        if check:
            self.coords = args
            self.coords = list(
                map(lambda x: [x[0], x[1], x[2] * 2, x[3] * 2, x[4]],
                    self.coords))
        else:
            self.coords = ROAD2[choice([0, 1])]

        self.pos = 0
        self.hp = 30
        self.image1 = Evil2.image
        self.image2 = Evil2.image2
        self.image = self.image1
        self.rect = self.image2.get_rect()
        self.rect.x, self.rect.y, self.d_x, self.d_y, flip = self.coords[
            self.pos]

    def update(self, gun_sprites, Evil2_sprites, player, event1, event2, V1, V2, MONEY):
        self.image = self.image2 if self.image == self.image1 else self.image1
        if (self.rect.x == self.coords[self.pos + 1][0] or self.rect.x ==
            self.coords[self.pos + 1][0] - 1) and (
                self.rect.y == self.coords[self.pos + 1][1] or self.rect.y ==
                self.coords[self.pos + 1][1] - 1):
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
            Evil2_sprites.remove(self)
            MONEY.play()
            player.money += 10
            player.points += 1
            if player.points % 10 == 0:
                V1 = V1 // 2
                V2 = V2 // 2
                pygame.time.set_timer(event1, V1)
                pygame.time.set_timer(event2, V2)


class Backgroung:
    def __init__(self, flag=True):
        self.x = 0
        self.y = 0
        if flag:
            self.image = load_image("fonmain.png")
            self.image = pygame.transform.scale(self.image, (1080, 720))
        else:
            self.image = load_image("fonmain.png")
            self.image = pygame.transform.scale(self.image, (2160, 1440))

    def draw(self, screen, clear=False):
        if clear:
            self.image = load_image("background.jpg")
            self.image = pygame.transform.scale(self.image, (1080, 720))
            screen.blit(self.image, (0, 0))
        else:
            screen.blit(self.image, (self.x, self.y))


class City:


    def __init__(self, screen, flag=True):
        self.images = [pygame.transform.scale(load_image("city/city1.png"), (1080, 720)),
                       pygame.transform.scale(load_image("city/city2.png"), (1080, 720)),
                       pygame.transform.scale(load_image("city/city3.png"), (1080, 720))]
        self.images2 = [pygame.transform.scale(load_image("city/city1.png"), (2160, 1440)),
                        pygame.transform.scale(load_image("city/city2.png"), (2160, 1440)),
                        pygame.transform.scale(load_image("city/city3.png"), (2160, 1440))]
        self.x = 0
        self.y = 0
        self.flag = flag
        self.status = "UP"
        self.statusi = 1
        if self.flag:
            self.image = self.images[self.statusi]
        else:
            self.image = self.images2[self.statusi]
        screen.blit(self.image, (self.x, self.y))

    def cheageimage(self):
        if self.status == "UP":
            self.statusi += 1
            if self.statusi == 2:
                self.status = "DOWN"
        else:
            self.statusi -= 1
            if self.statusi == 0:
                self.status = "UP"
        if self.flag:
            self.image = self.images[self.statusi]
        else:
            self.image = self.images2[self.statusi]

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class Sea:

    def __init__(self, screen, flag=True):
        self.images = [pygame.transform.scale(load_image("sea/sea1.png"), (1080, 720)),
                       pygame.transform.scale(load_image("sea/sea2.png"), (1080, 720)),
                       pygame.transform.scale(load_image("sea/sea3.png"), (1080, 720))]
        self.images2 = [pygame.transform.scale(load_image("sea/sea1.png"), (2160, 1440)),
                        pygame.transform.scale(load_image("sea/sea2.png"), (2160, 1440)),
                        pygame.transform.scale(load_image("sea/sea3.png"), (2160, 1440))]
        self.x = 0
        self.y = 0
        self.flag = flag
        self.status = "UP"
        self.statusi = 1
        if self.flag:
            self.image = self.images[self.statusi]
        else:
            self.image = self.images2[self.statusi]
        screen.blit(self.image, (self.x, self.y))

    def cheageimage(self):
        if self.status == "UP":
            self.statusi += 1
            if self.statusi == 2:
                self.status = "DOWN"
        else:
            self.statusi -= 1
            if self.statusi == 0:
                self.status = "UP"
        if self.flag:
            self.image = self.images[self.statusi]
        else:
            self.image = self.images2[self.statusi]

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class Electro:

    def __init__(self, screen, flag=True):
        self.images = [pygame.transform.scale(load_image("electro/electro1.png"), (1080, 720)),
                       pygame.transform.scale(load_image("electro/electro2.png"), (1080, 720)),
                       pygame.transform.scale(load_image("electro/electro3.png"), (1080, 720))]
        self.images2 = [pygame.transform.scale(load_image("electro/electro1.png"), (2160, 1440)),
                        pygame.transform.scale(load_image("electro/electro2.png"), (2160, 1440)),
                        pygame.transform.scale(load_image("electro/electro3.png"), (2160, 1440))]
        self.x = 0
        self.y = 0
        self.flag = flag
        self.status = "UP"
        self.statusi = 1
        if self.flag:
            self.image = self.images[self.statusi]
        else:
            self.image = self.images2[self.statusi]
        screen.blit(self.image, (self.x, self.y))

    def cheageimage(self):
        if self.status == "UP":
            self.statusi += 1
            if self.statusi == 2:
                self.status = "DOWN"
        else:
            self.statusi -= 1
            if self.statusi == 0:
                self.status = "UP"
        if self.flag:
            self.image = self.images[self.statusi]
        else:
            self.image = self.images2[self.statusi]

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
