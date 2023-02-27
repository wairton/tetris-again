import pygame

import sys
import configuration.config as config
import color
import json
from .base import Context


class ConfigPlayerContext(Context):
    def __init__(self, drawer):
        super(ConfigPlayerContext, self).__init__(drawer)

    def draw_options(self):
        self.drawer.fill(color.BLACK)
        try:
            configuration = json.load(open(config.OPTIONS_FILE))
        except Exception as e:
            print(e)

        screen_w, screen_h = config.SCREEN_RESOUTION
        font = pygame.font.Font(config.FONT_FILE, 40)
        # List used to track which options to set and which keys are being used
        list_of_options = []
        list_of_used_keys = ["return", "escape"]
        # Drawing the options and their respective cubes
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
            confirm_font = font.render("Press Enter to confirm", 1, color.WHITE, color.BLACK)
        self.drawer.blit(
            confirm_font,
            ((screen_w - confirm_font.get_width()) / 2, screen_h - 50)
        )
        self.execute(list_of_options, list_of_used_keys)

    def execute(self, options, keys_used):

        fpsClock = pygame.time.Clock()
        screen_w, screen_h = config.SCREEN_RESOUTION
        width_pos = screen_w / 10
        font = pygame.font.Font(config.FONT_FILE, 40)
        setting_key = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:

                    for option in options:
                        # Checking which option the user Clicked
                        if option.check_collision(pygame.mouse.get_pos()):
                            setting_key = True
                            new_key_option = option
                            # Changing the color to yellow for better User Experience
                            height_pos = (new_key_option.count * 100) + 50
                            new_key_option.surface.fill(color.YELLOW)
                            self.drawer.blit(
                                option.surface,
                                (width_pos, height_pos)
                            )
                            self.drawer.blit(
                                font.render(new_key_option.key, 1, color.YELLOW, color.BLACK),
                                (width_pos + 100, height_pos)
                            )

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                    if event.key == pygame.K_RETURN:
                        # Dumping the new options (or old if no changes are made) to JSON
                        dumpdict = {}

                        for option in options:
                            dumpdict[option.option] = option.key
                        json_dump = json.dumps(dumpdict)

                        with open(config.OPTIONS_FILE, "w") as file:
                            file.write(json_dump)

                    if setting_key is True:
                        if pygame.key.name(event.key) not in keys_used:
                            # Removing the existing key to the used keys list
                            # and adding the new one
                            keys_used.remove(new_key_option.key)
                            keys_used.append(pygame.key.name(event.key))
                            new_key_option.key = pygame.key.name(event.key)

                            # Erasing the existing text
                            eraser_box = pygame.Surface((screen_w, 100))
                            eraser_box.fill(color.BLACK)
                            self.drawer.blit(
                                eraser_box,
                                (width_pos + 100, (new_key_option.count * 100) + 50)
                            )
                            self.drawer.blit(
                                eraser_box,
                                (0, 0)
                            )
                            # Changing the color to white to represent set option.
                            new_key_option.surface.fill(color.WHITE)
                            self.drawer.blit(
                                new_key_option.surface,
                                (width_pos, height_pos)
                            )
                            self.drawer.blit(
                                font.render(str(new_key_option.key), 1, color.WHITE, color.BLACK),
                                (width_pos + 100, (new_key_option.count * 100) + 50)
                            )
                            setting_key = False
                        else:
                            # In case that the key is already used, show error.
                            error_font = font.render(
                                "Key already set",
                                1,
                                color.RED
                            )
                            self.drawer.blit(
                                error_font,
                                ((screen_w - error_font.get_width()) / 2, 0)
                            )

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
