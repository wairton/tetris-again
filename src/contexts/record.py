import sys

import pygame
import pygame.locals as pl

import config
import color
from .base import Context


class RecordContext(Context):
    def __init__(self, drawer):
        super(RecordContext, self).__init__(drawer)

    def execute(self):
        try:
            records = list(map(int, open(config.RECORD_FILE).readlines()))
        except Exception as e:
            print("TODO =)", e)
        print(records)
        self.drawer.fill(color.BEAUTIFUL_BLUE)
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
