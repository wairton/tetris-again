import sys

import pygame

from draw import Draw
import config
from highscore import highscore


class Game:
    def __init__(self):
        pygame.init()
        self.draw = Draw(pygame.display.set_mode(config.SCREEN_RESOUTION))
        pygame.display.set_caption(config.GAME_WINDOW_TITLE)

    def loop(self):
        import contexts as ctx
        ctx.IntroContext(self.draw).execute()
        next_option = None
        context_data = {}
        while True:
            if next_option:
                option = next_option
                next_option = None
            else:
                option = ctx.MainMenuContext(self.draw).execute()

            if option == 'exit':
                sys.exit()
            elif option == 'play':
                score = ctx.PlayContext(self.draw).execute()
                if highscore.is_highscore(score):
                    next_option = 'records'
                    context_data = {
                        'new_highscore': score
                    }
            elif option == 'records':
                ctx.RecordContext(self.draw).execute(**context_data)
            elif option == 'options':
                # TODO
                pass
                # ctx.ConfigPlayerContext(self.draw).draw_space()
            else:
                print(option, 'unknown')


if __name__ == '__main__':
    Game().loop()
