import time
import sys

import pygame
import pygame.locals as pl

import config
import color as cl
from mechanics import GameScreen


class Context(object):
    def __init__(self, drawer):
        self.drawer = drawer

    def execute(self):
        raise NotImplementedError


class IntroContext(Context):
    def __init__(self, drawer):
        super(IntroContext, self).__init__(drawer)

    def execute(self):
        logo = pygame.image.load(config.IMG_LOGO)
        self.drawer.fill(cl.BEATIFUL_BLUE)
        # soundObj = pygame.mixer.Sound('thundar.wav')
        # soundObj.play()
        x, y = config.SCREEN_RESOUTION
        logo_width = logo.get_width()
        self.drawer.blit(logo, ((x - logo_width) / 2, y / 3))
        self.drawer.display()
        time.sleep(2)
        self.drawer.fill(cl.BLACK)
        self.drawer.display()
        return 0


class MainMenuContext(Context):
    def __init__(self, drawer):
        super(MainMenuContext, self).__init__(drawer)
        self.selected_option = 0
        self.options = ['play', 'versus', 'options', 'records', 'exit']

    def execute(self):
        self.button = pygame.image.load(config.IMG_BUTTON)
        self.button_sel = pygame.image.load(config.IMG_BUTTON_SEL)
        while True:
            self.drawMenu()
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

    def drawMenu(self):
        screen_w, screen_h = config.SCREEN_RESOUTION
        button_w, button_h = self.button.get_size()
        x_pad = (screen_w - button_w) / 2
        y_pad = screen_h - (button_h + 10) * len(self.options)
        option_size = button_h + 5
        self.drawer.fill(cl.BEATIFUL_BLUE)
        font = pygame.font.Font(None, 50)
        for i, option in enumerate(self.options):
            y_pos = y_pad + option_size * i
            text = font.render(option, 1, (20, 20, 20))
            if i == self.selected_option:
                self.drawer.blit(self.button_sel, (x_pad, y_pos))
            else:
                self.drawer.blit(self.button, (x_pad, y_pos))
            text_x_pos = (button_w - text.get_width()) / 2 + x_pad
            text_y_pos = (button_h - text.get_height()) / 2 + y_pos
            self.drawer.blit(text, (text_x_pos, text_y_pos))
        self.drawer.display()


class PlayContext(Context):
    def __init__(self, drawer):
        super(PlayContext, self).__init__(drawer)

    def execute(self):
        game_screen = GameScreen(self.drawer, (10, 60))
        i, mod = 0, 8
        FPS = 32  # frames per second setting
        morreu = False
        while True:
            i += 1
            fpsClock = pygame.time.Clock()
            for event in pygame.event.get():
                if event.type == pl.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pl.KEYDOWN:
                    if event.key == pl.K_ESCAPE:
                        return 'foo'
                    elif event.key == pl.K_UP:
                        game_screen.loop('rotate')
                    elif event.key == pl.K_DOWN:
                        mod = 2
                    elif event.key == pl.K_LEFT:
                        game_screen.loop('left')
                    elif event.key == pl.K_RIGHT:
                        game_screen.loop('right')
                    elif event.key == pl.K_SPACE:
                        game_screen.loop('ground')
                if event.type == pl.KEYUP:
                    if event.key == pl.K_DOWN:
                        mod = 8
            if i % mod == 0:
                morreu = game_screen.loop()
                i = 0
            pygame.display.update()
            if morreu:
                return 'foo'
            fpsClock.tick(FPS)


class RecordContext(Context):
    def __init__(self, drawer):
        super(RecordContext, self).__init__(drawer)

    def execute(self):
        try:
            records = list(map(int, open(config.RECORD_FILE).readlines()))
        except Exception as e:
            print("TODO =)", e)
        print(records)
        self.drawer.fill(cl.BEATIFUL_BLUE)
        screen_w, screen_h = config.SCREEN_RESOUTION
        FPS = 32  # frames per second setting
        font = pygame.font.Font(None, 40)
        while True:
            fpsClock = pygame.time.Clock()
            for event in pygame.event.get():
                if event.type == pl.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pl.KEYDOWN:
                    return 'foo'
            for i in range(len(records)):
                msg = "{}. {}".format(i + 1, records[i])
                text = font.render(msg, 1, (20, 20, 20))
                text_x_pos = (screen_w - text.get_width()) / 2
                self.drawer.blit(
                    text, (text_x_pos, (text.get_height() + 2) * i + 50))
            fpsClock.tick(FPS)
            self.drawer.display()
