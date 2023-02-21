import pygame
import pygame.locals as pl

import sys
import configuration.config as config
import color
import json
from .base import Context


class ConfigPlayerContext(Context):
    def __init__(self, drawer):
        super(ConfigPlayerContext, self).__init__(drawer)

    def execute(self):
        self.drawer.fill(color.BLACK)

        try:
            configuration = json.load(open(config.OPTIONS_FILE))
        except Exception as e:
            print(e)

        screen_w, screen_h = config.SCREEN_RESOUTION
        font = pygame.font.Font(config.FONT_FILE, 40)
        # Drawing the rects
        for count, options in enumerate(configuration):
            rect = pygame.Surface((50, 50))
            rect.fill(color.WHITE)
            self.drawer.blit(
                rect,
                (screen_w / 10, (count * 100) + 50)
            )
            option_font = font.render(configuration[options], 1, color.WHITE)
            self.drawer.blit(
                option_font,
                ((screen_w / 10) + 100, (count * 100) + 50)
            )

        while True:
            for event in pygame.event.get():
                pygame.display.flip()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
