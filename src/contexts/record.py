import sys

import pygame
import pygame.locals as pl

import config
import color
import json
from .base import Context


class RecordContext(Context):
    def __init__(self, drawer):
        super(RecordContext, self).__init__(drawer)

    def execute(self):

        # Opening the JSON and setting the screen
        try:
            records = json.load(open(config.RECORD_FILE))
        except Exception as e:
            print("TODO =)", e)

        self.drawer.fill(color.BEAUTIFUL_BLUE)
        screen_w, screen_h = config.SCREEN_RESOUTION

        FPS = 32  # frames per second setting
        font = pygame.font.Font(None, 40)
        fpsClock = pygame.time.Clock()

        # Getting the highscore table and print it
        for count, highscore in enumerate(records):
            msg = "{}. {} {}".format(count + 1, highscore['name'], highscore['score'])
            text = font.render(msg, 1, (20, 20, 20))
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
        try:
            records = json.load(open(config.RECORD_FILE))
        except Exception as e:
            print(e)

        if len(records) < config.RECORD_SIZE:
            self.draw_new_highscore(score)
            return 'No matter'

        for highscore in records:
            if score > highscore['score']:
                self.draw_new_highscore(score)
                break
        return 'It just works'

    def draw_new_highscore(self, score):
        self.drawer.fill(color.BLACK)
        screen_w, screen_h = config.SCREEN_RESOUTION
        font = pygame.font.Font('Fixedsys Excelsior 3.01 Regular.ttf', 40)

        try:
            records = json.load(open(config.RECORD_FILE))
        except Exception as e:
            print(e)
        if len(records) >= config.RECORD_SIZE:
            records.pop()

        records.append({'name': '___', 'score': score})
        records.sort(reverse=True, key=self.sort_by_score)

        title = 'New Highscore!'
        title_font = font.render(title, 1, color.WHITE)
        centered_text = (screen_w - title_font.get_width()) / 2
        self.drawer.blit(
            title_font, (centered_text, 50)
        )

        for count, highscore in enumerate(records):
            msg = "{}. {} {}".format(count + 1, highscore['name'], str(highscore['score']).zfill(9))
            text = font.render(msg, 1, color.WHITE)
            text_x_pos = (screen_w - text.get_width()) / 2
            self.drawer.blit(text,
                             (text_x_pos, (text.get_height() + 2) * count + 100)
                             )
            if highscore['name'] == '___':
                new_score_x_pos = (screen_w - text.get_width()) / 2
                new_score_y_pos = (text.get_height() + 2) * count + 100
                new_count = count + 1
        self.new_highscore(score, new_score_x_pos, new_score_y_pos, new_count)

    def new_highscore(self, score, new_x, new_y, new_count):

        in_nick_msg = '___'
        highscore_nick = ''
        FpsClock = pygame.time.Clock()
        screen_w, screen_h = config.SCREEN_RESOUTION
        font = pygame.font.Font('Fixedsys Excelsior 3.01 Regular.ttf', 40)
        msg = "{}. {} {}".format(new_count, in_nick_msg, str(score).zfill(9))

        try:
            records = json.load(open(config.RECORD_FILE))
        except Exception as e:
            print(e)

        text_color = color.BLACK

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if len(highscore_nick) == 3:
                        records.append({'name': highscore_nick, 'score': score})
                        records.sort(reverse=True, key=self.sort_by_score)

                        new_highscore = json.dumps(records, sort_keys=True)
                        with open('records.json', 'w') as f:
                            f.write(new_highscore)
                        return 'Goodbye!'
                    if event.unicode.isalpha():
                        highscore_nick += str(event.unicode).upper()
                        in_nick_msg = in_nick_msg.replace('_', str(event.unicode).upper(), 1)
                        msg = "{}. {} {}".format(new_count, in_nick_msg, str(score).zfill(9))
                        text = font.render(msg, 1, color.WHITE)
                        self.drawer.blit(text,
                                         (new_x, new_y)
                                         )
            if text_color == color.YELLOW:
                text = font.render(msg, 1, text_color)
                self.drawer.blit(text,
                                 (new_x, new_y)
                                 )
                text_color = color.WHITE
            else:
                text = font.render(msg, 1, text_color)
                self.drawer.blit(text,
                                 (new_x, new_y)
                                 )
                text_color = color.YELLOW
            FpsClock.tick(2)
            self.drawer.display()

    def sort_by_score(self, score):
        return score['score']
