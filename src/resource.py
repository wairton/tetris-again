import os

import pygame

from configuration.config import IMG_PATH
from images import image_loader

# menu
IMG_LOGO = os.path.join(IMG_PATH, 'logo_.png')
IMG_BUTTON = os.path.join(IMG_PATH, 'menu_.png')
IMG_BUTTON_SEL = os.path.join(IMG_PATH, 'menu_selected_2.png')

# Block files
BLACK_BLOCK = os.path.join(IMG_PATH, 'block_black.png')
BLUE_BLOCK = os.path.join(IMG_PATH, 'block_blue.png')
GREEN_BLOCK = os.path.join(IMG_PATH, 'block_green.png')
INDIGO_BLOCK = os.path.join(IMG_PATH, 'block_indigo.png')
LIGHT_BLUE_BLOCK = os.path.join(IMG_PATH, 'block_light_blue.png')
ORANGE_BLOCK = os.path.join(IMG_PATH, 'block_orange.png')
RED_BLOCK = os.path.join(IMG_PATH, 'block_red.png')
YELLOW_BLOCK = os.path.join(IMG_PATH, 'block_yellow.png')

BLOCKS_PATH = [
    BLACK_BLOCK, BLUE_BLOCK, GREEN_BLOCK,
    INDIGO_BLOCK, LIGHT_BLUE_BLOCK, ORANGE_BLOCK,
    RED_BLOCK, YELLOW_BLOCK
]

BLOCKS_IMG = [image_loader(block) for block in BLOCKS_PATH]

GAME_FONT = pygame.font.Font(None, 30)  # TODO: remove this hard coded value!
