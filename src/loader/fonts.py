import config

import pygame


class Fonts:
    FIXED = 'Fixedsys Excelsior 3.01 Regular.ttf'


def load_font(size):
    return pygame.font.Font(f"{config.FONTS_PATH}/{Fonts.FIXED}", size)