import pygame
import pygame.locals as pl

import sys
import config
import color
import json
from .base import Context


class ConfigPlayerContext(Context):
    def __init__(self, drawer):
        super(ConfigPlayerContext, self).__init__(drawer)

    def execute(self):
        self.drawer.fill(color.BLACK)
        # try:
        #    json.load(open())

        while True:
            for event in pygame.event.get():
                pygame.display.flip()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
