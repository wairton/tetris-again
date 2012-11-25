import color
import os

#game main settings
GAME_WINDOW_TITLE = "Tetris Again"
GAME_FPS = 32
SCREEN_RESOUTION = (470, 600)
#game image settings
IMG_PATH = os.path.join(os.getcwd(), 'img')
IMG_LOGO = os.path.join(IMG_PATH, 'logo_.png')
IMG_BUTTON = os.path.join(IMG_PATH, 'menu_.png')
IMG_BUTTON_SEL = os.path.join(IMG_PATH, 'menu_selected_2.png')
#in game settings
LINE_VALUE = (100, 300, 500, 800)
#grid settings
GRID_POSITION = (20, 20)
GRID_WIDTH = 10
GRID_HEIGHT = 20
GRID_EMPTY_COLOR = color.BLACK
GRID_BORDER_COLOR = color.WHITE
GRID_PAD = 2
#block settings
BLOCK_SIZE = 25
BLOCK_PAD = 1


