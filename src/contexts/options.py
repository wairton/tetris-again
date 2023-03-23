import sys
import json
import pygame

import configuration.config as config
import color
from .base import Context
from data.dataclasses.controller import Controller

TEXT_INCREMENT = 60
RESERVED_KEYS = ["esc", "enter"]
BUTTON_IMAGES = [config.ROTATE_BUTTON,
                 config.ANTI_ROTATE_BUTTON,
                 config.DOWN_BUTTON,
                 config.LEFT_BUTTON,
                 config.RIGHT_BUTTON,
                 config.GROUND_BUTTON,
                 config.HOLD_BUTTON]
screen_w, screen_h = config.SCREEN_RESOUTION


class ConfigPlayerContext(Context):
    def __init__(self, drawer):
        super(ConfigPlayerContext, self).__init__(drawer)
        self.controller = Controller()

    def draw_options(self):
        self.drawer.fill(color.BLACK)
        configuration = self.controller.load()

        font = pygame.font.Font(config.FONT_FILE, 40)
        # List used to track which options to set and which keys are being used
        list_of_options = []
        width_pos = (screen_w / 100) * 5
        # Drawing the options and their respective cubes
        for count, player in enumerate(configuration):
            height_pos = 50
            width_pos = ((screen_w / 10) // len(configuration)) + (screen_w / 100) * ((100 / len(configuration)) * count)
            option_enumeration = 0
            self.drawer.line(
                color.WHITE,
                ((screen_w / len(configuration) - 10) * count + 1, 50),
                ((screen_w / len(configuration) - 10) * count + 1, screen_h)
            )
            list_of_options.append([])
            for img_count, value in enumerate(configuration[player].__dict__.items()):

                atr, key = value
                option = Option(
                    height_pos,
                    width_pos,
                    atr,
                    key,
                    height_pos,
                    self.drawer,
                    self.controller,
                    img_count
                )

                option.set_surface()

                option.set_text(color.WHITE)

                list_of_options[count].append(option)
                height_pos += (screen_h / 100) * (100 / 10)
                option_enumeration += 1
        confirm_font = font.render("Press Enter to confirm", 1, color.WHITE, color.BLACK)
        self.drawer.blit(
            confirm_font,
            ((screen_w - confirm_font.get_width()) / 2, screen_h - 40)
        )
        self.execute(list_of_options)

    def execute(self, players):
        fps_clock = pygame.time.Clock()
        font = pygame.font.Font(config.FONT_FILE, 40)
        setting_key = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # After clicking in a setting box; It views if it is already setting another key.
                    # if not, it views which player and option the user is changing
                    if setting_key is False:
                        for player in players:
                            for option in player:
                                if option.check_collision(pygame.mouse.get_pos()):
                                    setting_key = True
                                    new_key_option = option
                                    new_key_option.surface.fill(color.YELLOW)
                                    new_key_option.set_surface()
                                    new_key_option.set_text(color.YELLOW)
                    else:
                        eraser_box = pygame.Surface((screen_w, 50))
                        eraser_box.fill(color.BLACK)
                        self.drawer.blit(
                            eraser_box,
                            (0, 0)
                        )
                        error_font = font.render(
                            "Already selecting a key",
                            1,
                            color.RED
                        )
                        self.drawer.blit(
                            error_font,
                            ((screen_w - error_font.get_width()) / 2, 0)
                        )
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                    if event.key == pygame.K_RETURN:
                        self.controller.save()
                        return

                    if setting_key is True:
                        if not self.controller.is_key_used(pygame.key.name(event.key)):
                            new_key_option.change_key(pygame.key.name(event.key))

                            new_key_option.erase_text()
                            eraser_box = pygame.Surface((screen_w, 50))
                            eraser_box.fill(color.BLACK)
                            self.drawer.blit(
                                eraser_box,
                                (0, 0)
                            )
                            new_key_option.surface.fill(color.WHITE)
                            new_key_option.set_surface()
                            new_key_option.set_text(color.WHITE)
                            setting_key = False
                        else:
                            if pygame.key.name(event.key) not in RESERVED_KEYS:
                                for player in players:
                                    for option in player:
                                        if option.key == pygame.key.name(event.key):
                                            option.change_key(new_key_option.key)
                                            option.erase_text()
                                            option.set_text(color.WHITE)
                                            break
                                new_key_option.change_key(pygame.key.name(event.key))
                                new_key_option.surface.fill(color.WHITE)
                                new_key_option.erase_text()
                                new_key_option.set_surface()
                                new_key_option.set_text(color.WHITE)
                                setting_key = False
                            else:
                                eraser_box = pygame.Surface((screen_w, 50))
                                eraser_box.fill(color.BLACK)
                                self.drawer.blit(
                                    eraser_box,
                                    (0, 0)
                                )
                                error_font = font.render(
                                    "Key reserved",
                                    1,
                                    color.RED
                                )
                                self.drawer.blit(
                                    error_font,
                                    ((screen_w - error_font.get_width()) / 2, 0)
                                )

            pygame.display.flip()
            fps_clock.tick(60)


class Option:
    def __init__(self, height, width, atr, key, text_height, drawer, controller, count):
        self.height = height
        self.width = width
        self.atr = atr
        self.key = key
        self.drawer = drawer
        self.count = count
        self.controller = controller
        self.text_height = text_height
        self.surface = pygame.Surface((50, 50))
        self.rect = self.surface.get_rect(topleft=(width, height))
        self.surface.fill(color.WHITE)

    def check_collision(self, pos):
        return self.rect.collidepoint(pos)

    def set_surface(self):
        self.drawer.blit(
            self.surface,
            (self.width, self.height)
        )
        self.drawer.blit(
            pygame.image.load(BUTTON_IMAGES[self.count]),
            (self.width, self.height)
        )

    def set_text(self, text_color):
        font = pygame.font.Font(config.FONT_FILE, 40)
        self.drawer.blit(
            font.render(str(self.key), 1, text_color, color.BLACK),
            (self.width + TEXT_INCREMENT, self.text_height)
        )

    def erase_text(self):
        eraser_box = pygame.Surface(((screen_w / 100) * 30, 50))
        eraser_box.fill(color.BLACK)
        self.drawer.blit(
            eraser_box,
            (self.width + TEXT_INCREMENT, self.text_height)
        )

    def change_key(self, new_key):
        self.controller.key_change(self.atr, self.key, new_key)
        self.key = new_key
