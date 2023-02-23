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
        fpsClock = pygame.time.Clock()

        try:
            configuration = json.load(open(config.OPTIONS_FILE))
        except Exception as e:
            print(e)

        screen_w, screen_h = config.SCREEN_RESOUTION
        font = pygame.font.Font(config.FONT_FILE, 40)
        # Drawing the rects
        list_of_options = []
        list_of_used_keys = ["return", "escape"]
        for count, options in enumerate(configuration):

            option = Option(options, count, configuration[options])

            height_pos = (count * 100) + 50
            width_pos = screen_w / 10
            self.drawer.blit(
                option.surface,
                (width_pos, height_pos)
            )
            self.drawer.blit(
                font.render(option.key, 1, color.WHITE, color.BLACK),
                (width_pos + 100, height_pos)
            )
            list_of_options.append(option)
            list_of_used_keys.append(configuration[options])
        setting_key = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for option in list_of_options:
                        if option.check_collision(pygame.mouse.get_pos()):
                            setting_key = True
                            new_key_option = option
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if setting_key is True:
                        if event.key not in list_of_used_keys:
                            new_key_option.key = pygame.key.name(event.key)
                            print(new_key_option.key)
                            # Erasing the existing text
                            eraser_box = pygame.Surface((100, 100))
                            eraser_box.fill(color.BLACK)
                            self.drawer.blit(
                                eraser_box,
                                (width_pos + 100, (new_key_option.count * 100) + 50)
                            )
                            self.drawer.blit(
                                font.render(str(new_key_option.key), 1, color.WHITE, color.BLACK),
                                (width_pos + 100, (new_key_option.count * 100) + 50)
                            )
                            setting_key = False
            pygame.display.flip()
            fpsClock.tick(32)


class Option():
    def __init__(self, option, count, key):

        screen_w, screen_h = config.SCREEN_RESOUTION
        height_pos = (count * 100) + 50

        width_pos = screen_w / 10
        self.option = option
        self.key = key
        self.count = count
        self.surface = pygame.Surface((50, 50))
        self.rect = self.surface.get_rect(topleft=(width_pos, height_pos))
        self.surface.fill(color.WHITE)

    def check_collision(self, pos):
        if self.rect.collidepoint(pos):
            return True
        return False
