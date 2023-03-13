import pygame
import pygame.locals as pl

import configuration.config as config
from .base import Context
import color

from images import image_loader


class MainMenuContext(Context):
    def __init__(self, drawer):
        super(MainMenuContext, self).__init__(drawer)
        self.selected_option = 0
        self.options = ['play', 'versus', 'options', 'records', 'exit']

    def execute(self):
        self.button = image_loader(config.IMG_BUTTON)
        self.button_sel = image_loader(config.IMG_BUTTON_SEL)
        while True:
            self.draw_menu()
            for event in pygame.event.get():
                if event.type != pygame.KEYDOWN:
                    continue
                if event.key in [pl.K_DOWN, pl.K_RIGHT]:
                    self.selected_option += 1
                    self.selected_option %= len(self.options)
                elif event.key in [pl.K_UP, pl.K_LEFT]:
                    self.selected_option += len(self.options) - 1
                    self.selected_option %= len(self.options)
                elif event.key == pl.K_ESCAPE:
                    return 'exit'
                elif event.key == pl.K_RETURN:
                    return self.options[self.selected_option]

    def draw_menu(self):
        screen_w, screen_h = config.SCREEN_RESOUTION
        button_w, button_h = self.button.size
        x_pad = (screen_w - button_w) / 2
        y_pad = screen_h - (button_h + 10) * len(self.options)
        option_size = button_h + 5
        self.drawer.fill(color.BEAUTIFUL_BLUE)
        font = pygame.font.Font(None, 50)
        for i, option in enumerate(self.options):
            y_pos = y_pad + option_size * i
            text = font.render(option, 1, color.DARK_GRAY)
            if i == self.selected_option:
                self.drawer.blit(self.button_sel.surface, (x_pad, y_pos))
            else:
                self.drawer.blit(self.button.surface, (x_pad, y_pos))
            text_x_pos = (button_w - text.get_width()) / 2 + x_pad
            text_y_pos = (button_h - text.get_height()) / 2 + y_pos
            self.drawer.blit(text, (text_x_pos, text_y_pos))
        self.drawer.display()
