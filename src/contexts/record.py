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
        self.drawer.fill(color.BEAUTIFUL_BLUE)
        screen_w, screen_h = config.SCREEN_RESOUTION
        FPS = 32  # frames per second setting
        font = pygame.font.Font(None, 40)
        fpsClock = pygame.time.Clock()
        for i in range(len(records)):
            msg = "{}. {}".format(i + 1, records[i])
            text = font.render(msg, 1, (20, 20, 20))
            text_x_pos = (screen_w - text.get_width()) / 2
            self.drawer.blit(
                text, (text_x_pos, (text.get_height() + 2) * i + 50))
        while True:
            for event in pygame.event.get():
                if event.type == pl.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pl.KEYDOWN:
                    return 'foo'
            fpsClock.tick(FPS)
            self.drawer.display()

    def newRecord(self, score):
        print(score)
        self.drawer.fill(color.BEAUTIFUL_BLUE)
        screen_w, screen_h = config.SCREEN_RESOUTION
        fpsClock = pygame.time.Clock()
        font = pygame.font.Font(None, 40)
        nick = ''

        title = 'Insert your nickname!'
        title_font = font.render(title, 1, (20, 20, 20))
        centered_text = (screen_w - title_font.get_width()) / 2
        self.drawer.blit(
            title_font, (centered_text, 100)
        )

        while True:
            for event in pygame.event.get():
                if event.type == pl.KEYDOWN:
                    if event.key == pl.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.unicode:
                        if len(nick) < 3:
                            nick += str(event.unicode)
                            nick_font = font.render(nick, 1, (20, 20, 20))
                            self.drawer.blit(
                                nick_font, (centered_text, 200)
                            )
                        else:
                            # Whitespace for the list
                            nick += ' '
                            score_list = []
                            with open(config.RECORD_FILE) as file:
                                for line in file:
                                    # Splitting the string for the score
                                    score_list.append(line.split(' '))
                                    # Checking if the highscore beats another
                                for count, highscore in enumerate(score_list):
                                    if score > int(highscore[1]):
                                        print(count)
                                        score_list.insert(count - 1, [nick, score])
                                        score_list.pop()
                                        break
                            f = open(config.RECORD_FILE, 'w')
                            for highscore in score_list:
                                f.write(highscore[0] + ' ' + str(highscore[1]))
                            f.close()
                            return 'GO BACK TO THE PASS!'
            fpsClock.tick(32)
            self.drawer.display()
