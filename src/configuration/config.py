import os
from enum import Enum

import color


class Backend(Enum):
    PYGAME = 1
    OTHER = 2


BACKEND = Backend.PYGAME

# game main settings
GAME_WINDOW_TITLE = "Tetris Again"
GAME_FPS = 32
SCREEN_RESOUTION = (470, 600)
# game image settings
GAME_PATH = os.getcwd()
RES_PATH = os.path.join(GAME_PATH, 'res')
IMG_PATH = os.path.join(RES_PATH, 'img')
CONFIGURATION_PATH = os.path.join(GAME_PATH, 'configuration')
IMG_LOGO = os.path.join(IMG_PATH, 'logo_.png')
IMG_BUTTON = os.path.join(IMG_PATH, 'menu_.png')
IMG_BUTTON_SEL = os.path.join(IMG_PATH, 'menu_selected_2.png')
ROTATE_BUTTON = os.path.join(IMG_PATH, "Rotate.png")
FONTS_PATH = os.path.join(RES_PATH, 'fonts')
FONT_FILE = os.path.join(FONTS_PATH, 'Fixedsys Excelsior 3.01 Regular.ttf')
RECORD_FILE = os.path.join(CONFIGURATION_PATH, 'records.json')
OPTIONS_FILE = os.path.join(CONFIGURATION_PATH, 'control.json')
# in game settings
LINE_VALUE = (100, 300, 500, 800)
# grid settings
GRID_POSITION = (20, 20)
GRID_WIDTH = 10
GRID_HEIGHT = 20
GRID_EMPTY_COLOR = color.BLACK
GRID_BORDER_COLOR = color.WHITE
GRID_PAD = 2
# block settings
BLOCK_SIZE = 25
BLOCK_PAD = 1
RECORD_SIZE = 10
