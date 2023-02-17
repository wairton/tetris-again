import pygame
import pygame.locals as pl

import config
import color
import json
from .base import Context


class ConfigPlayerContext(Context):
    def __init__(self, drawer):
        super().__init__(drawer)

    def draw_space(self):
        self.drawer.fill(color.BLACK)
