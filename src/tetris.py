import sys

import pygame

from draw import Draw
import config


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
                ctx.PlayContext(self.draw).execute()
            elif option == 'records':
                ctx.RecordContext(self.draw).execute()
            else:
                print(option, 'unknown')


if __name__ == '__main__':
    Game().loop()
