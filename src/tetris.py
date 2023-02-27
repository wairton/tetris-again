import sys

import pygame

from draw import Draw
import configuration.config as config


class Game:
    def __init__(self):
        pygame.init()
        self.draw = Draw(pygame.display.set_mode(config.SCREEN_RESOUTION))
        pygame.display.set_caption(config.GAME_WINDOW_TITLE)

    def loop(self):
        import contexts as ctx
        ctx.IntroContext(self.draw).execute()
        while True:
            option = ctx.MainMenuContext(self.draw).execute()
            if option == 'exit':
                sys.exit()
            elif option == 'play':
                score = ctx.PlayContext(self.draw).execute()
                ctx.RecordContext(self.draw).check_if_highscore(score)
            elif option == 'records':
                ctx.RecordContext(self.draw).execute()
            elif option == 'options':
                ctx.ConfigPlayerContext(self.draw).draw_options()
            else:
                print(option, 'unknown')


if __name__ == '__main__':
    Game().loop()
