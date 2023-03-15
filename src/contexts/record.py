import pygame
import pygame.locals as pl

import configuration.config as config
import color
import sys

from loader import load_font
from .base import Context
from highscore import Highscore


class RecordContext(Context):
    def __init__(self, drawer):
        self.font = load_font(40)
        self.highscore = Highscore()
        super().__init__(drawer)

    def execute(self, new_highscore=None):
        if new_highscore is not None:
            self.draw_new_highscore(new_highscore)
            return ""
        self.drawer.fill(color.BEAUTIFUL_BLUE)
        screen_w, screen_h = config.SCREEN_RESOUTION

        FPS = 32  # frames per second setting
        font2 = pygame.font.Font(None, 40)
        fpsClock = pygame.time.Clock()

        # Getting the highscore table and print it
        for count, highscore in enumerate(self.highscore.scores):
            msg = "{}. {} {}".format(count + 1, highscore.name, highscore.score)
            text = font2.render(msg, 1, (20, 20, 20))
            text_x_pos = (screen_w - text.get_width()) / 2
            self.drawer.blit(
                text, (text_x_pos, (text.get_height() + 2) * count + 50))

        while True:
            for event in pygame.event.get():
                if event.type == pl.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pl.KEYDOWN:
                    return 'foo'
            fpsClock.tick(FPS)
            self.drawer.display()

    def check_if_highscore(self, score):
        if Highscore.is_highscore(score=score):
            self.draw_new_highscore(score)
        return True

    def draw_new_highscore(self, score):
        self.drawer.fill(color.BLACK)
        screen_w, screen_h = config.SCREEN_RESOUTION

        records = self.highscore.scores

        records.append(Highscore.ScoreItem(name='___', score=score))
        records = sorted(records, reverse=True, key=lambda s: s.score)

        title = 'New Highscore!'
        title_font = self.font.render(title, 1, color.WHITE)
        centered_text = (screen_w - title_font.get_width()) / 2
        self.drawer.blit(title_font, (centered_text, 0))

        for count, highscore in enumerate(records):
            msg = "{}. {} {}".format(count + 1, highscore.name, str(highscore.score).zfill(9))
            text = self.font.render(msg, 1, color.WHITE)
            text_x_pos = (screen_w - text.get_width()) / 2
            text_y_pos = (text.get_height() + 2) * count + 100
            self.drawer.blit(text, (text_x_pos, text_y_pos))
            if highscore.name == '___':
                new_score_x_pos = (screen_w - text.get_width()) / 2
                new_score_y_pos = (text.get_height() + 2) * count + 100
                new_count = count + 1
        self.new_highscore(score, new_score_x_pos, new_score_y_pos, new_count)

    def new_highscore(self, score, new_x, new_y, new_count):
        in_nick_msg = '___'
        highscore_nick = ''
        FpsClock = pygame.time.Clock()
        screen_w, screen_h = config.SCREEN_RESOUTION
        msg = "{}. {} {}".format(new_count, in_nick_msg, str(score).zfill(9))

        text_color = color.WHITE

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if len(highscore_nick) == 3 and event.key == pygame.K_RETURN:

                        self.highscore.add(name=highscore_nick, score=score)
                        self.highscore.save()
                        return ""

                    if event.unicode.isalpha() and len(highscore_nick) < 3:
                        highscore_nick += str(event.unicode).upper()
                        in_nick_msg = in_nick_msg.replace('_', str(event.unicode).upper(), 1)
                        msg = "{}. {} {}".format(new_count, in_nick_msg, str(score).zfill(9))
                        text = self.font.render(msg, 1, color.WHITE)
                        self.drawer.blit(text, (new_x, new_y))
                        if len(highscore_nick) == 3:
                            finish_text = 'Press Enter to Continue'
                            finish_font = self.font.render(finish_text, 1, color.WHITE)
                            centered_text = (screen_w - finish_font.get_width()) / 2
                            self.drawer.blit(
                                finish_font,
                                (centered_text, 50)
                            )
            if text_color == color.YELLOW:
                text = self.font.render(msg, 1, text_color)
                self.drawer.blit(text, (new_x, new_y))
                text_color = color.WHITE
            else:
                text = self.font.render(msg, 1, text_color)
                self.drawer.blit(text, (new_x, new_y))
                text_color = color.YELLOW
            FpsClock.tick(2)
            self.drawer.display()
