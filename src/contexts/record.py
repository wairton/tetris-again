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
            self.new_highscore(score)
            return 'No matter'

        for highscore in records:
            if score > highscore['score']:
                self.new_highscore(score)
                break
        return 'It just works'

    def new_highscore(self, score):
        self.drawer.fill(color.BEAUTIFUL_BLUE)
        screen_w, screen_h = config.SCREEN_RESOUTION
        font = pygame.font.Font(None, 40)

        try:
            records = json.load(open(config.RECORD_FILE))
        except Exception as e:
            print(e)
        if len(records) >= config.RECORD_SIZE:
            records.pop()
        records.append({'name': '___', 'score': score})
        records.sort(reverse=True, key=self.sort_by_score)
        title = 'Insert your nickname!'
        title_font = font.render(title, 1, (20, 20, 20))
        centered_text = (screen_w - title_font.get_width()) / 2
        self.drawer.blit(
            title_font, (centered_text, 50)
        )
        for count, highscore in enumerate(records):
            msg = "{}. {} {}".format(count + 1, highscore['name'], highscore['score'])
            text = font.render(msg, 1, (20, 20, 20))
            text_x_pos = (screen_w - text.get_width()) / 2
            self.drawer.blit(text,
                             (text_x_pos, (text.get_height() + 2) * count + 100))
            if highscore['name'] == '___':
                new_score_x_pos = (screen_w - text.get_width()) / 2
                new_score_y_pos = (text.get_height() + 2) * count + 100

        insert_nick_msg = '___'
        highscore_nick = ''

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if len(highscore_nick) == 3:
                        records.remove({'name': '___', 'score': score})
                        records.append({'name': highscore_nick, 'score': score})
                        records.sort(reverse=True, key=self.sort_by_score)

                        new_highscore = json.dumps(records, sort_keys=True)
                        with open('records.json', 'w') as f:
                            f.write(new_highscore)
                        return 'Goodbye!'
                    if event.unicode.isalpha():
                        highscore_nick += event.unicode
                        insert_nick_msg = insert_nick_msg.replace('_', event.unicode, 1)
                        text = font.render(insert_nick_msg, 1, (20, 20, 20))
                        self.drawer.blit(text,
                                         (new_score_x_pos + 25, new_score_y_pos)
                                         )
            self.drawer.display()

    def sort_by_score(self, score):
        return score['score']
