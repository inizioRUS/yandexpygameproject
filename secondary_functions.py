import os
import pygame
import random
from math import *

def load_image(name, colorkey=None):  # Загрузка картинок
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def count_coords(x1, y1, x2, y2):  # Расчет координат при стрельбе
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


def create_particles(position, particles, Particle):  # Создание анимации партиклов
    particle_count = 2
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers), particles)