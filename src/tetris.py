import sys

import pygame
from pygame.locals import *

import config
import color
from draw import Draw
from contexts import *


class Game(object):
    def __init__(self):
        pygame.init()
        self.draw = Draw(pygame.display.set_mode(config.SCREEN_RESOUTION))
        pygame.display.set_caption(config.GAME_WINDOW_TITLE)
        self.mainloop()

    def mainloop(self):
        IntroContext(self.draw).execute()
        while True:
            option = MainMenuContext(self.draw).execute()
            if option == 'exit':
                sys.exit()
            elif option == 'play':
                PlayContext(self.draw).execute()
            elif option == 'records':
                RecordContext(self.draw).execute()
            else:
                print option, 'unknown' 

if __name__ == '__main__':
    game = Game()
    game.mainloop()
