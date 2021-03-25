from collections import namedtuple


Color = namedtuple('Color', 'r g b')


WHITE = Color(255, 255, 255)
WHITE2 = Color(240, 240, 240)
GRAY = Color(200, 200, 200)
DARK_GRAY = Color(20, 20, 20)
BLACK = Color(0, 0, 0)
RED = Color(255, 50, 50)
RED2 = Color(255, 0, 0)
DARK_RED = Color(128, 0, 0)
ORANGE = Color(255, 165, 0)
DARK_ORANGE = Color(128, 82, 0)
YELLOW = Color(255, 255, 0)
DARK_YELLOW = Color(128, 128, 0)
GREEN = Color(30, 160, 30)
GREEN2 = Color(0, 128, 0)
DARK_GREEN = Color(0, 64, 0)
BLUE = Color(50, 50, 255)
BLUE2 = Color(0, 0, 255)
LIGHT_BLUE = Color(50, 200, 255)
DARK_LIGHT_BLUE = Color(30, 100, 240)
DARK_BLUE = Color(0, 0, 128)
INDIGO = Color(200, 50, 200)
DARK_INDIGO = Color(80, 50, 80)
BEAUTIFUL_BLUE = Color(70, 150, 190)


GRID_EMPTY_COLOR = BLACK
GRID_BORDER_COLOR = WHITE
