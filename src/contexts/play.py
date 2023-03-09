import sys

import pygame
import pygame.locals as pl

from mechanics import GameScreen
from .base import Context


class PlayContext(Context):

    def execute(self):
        game_screen = GameScreen(self.drawer, (10, 60))
        i, mod = 0, 8
        FPS = 32  # frames per second setting
        died = False
        fps_clock = pygame.time.Clock()
        while True:
            i += 1
            for event in pygame.event.get():
                if event.type == pl.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pl.KEYDOWN:
                    if event.key == pl.K_ESCAPE:
                        died, score = game_screen.loop(GameScreen.Action.STEP)
                        if score == None:
                            return 0
                        else:
                            return score
                    elif event.key == pl.K_UP:
                        game_screen.loop(GameScreen.Action.ROTATE)
                    elif event.key == pl.K_DOWN:
                        mod = 2
                    elif event.key == pl.K_LEFT:
                        game_screen.loop(GameScreen.Action.LEFT)
                    elif event.key == pl.K_RIGHT:
                        game_screen.loop(GameScreen.Action.RIGHT)
                    elif event.key == pl.K_h:
                        game_screen.loop(GameScreen.Action.HOLD)
                    elif event.key == pl.K_SPACE:
                        died, score = game_screen.loop(GameScreen.Action.GROUND)
                        if died:
                            return score
                if event.type == pl.KEYUP:
                    if event.key == pl.K_DOWN:
                        mod = 8
            if i % mod == 0:
                died, score = game_screen.loop(GameScreen.Action.STEP)
                i = 0
            pygame.display.update()
            if died:
                return score
            fps_clock.tick(FPS)
