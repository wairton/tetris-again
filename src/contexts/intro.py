import time

import pygame

import config
import color as cl
from .base import Context


class IntroContext(Context):
    def __init__(self, drawer):
        super().__init__(drawer)

    def execute(self):
        logo = pygame.image.load(config.IMG_LOGO)
        self.drawer.fill(cl.BEAUTIFUL_BLUE)
        x, y = config.SCREEN_RESOUTION
        logo_width = logo.get_width()
        self.drawer.blit(logo, ((x - logo_width) / 2, y / 3))
        self.drawer.display()
        time.sleep(2)
        self.drawer.fill(cl.BLACK)
        self.drawer.display()
        return 0
