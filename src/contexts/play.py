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
        while True:
            i += 1
            fps_clock = pygame.time.Clock()
            for event in pygame.event.get():
                if event.type == pl.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pl.KEYDOWN:
                    if event.key == pl.K_ESCAPE:
                        return 'foo'
                    elif event.key == pl.K_UP:
                        game_screen.loop(GameScreen.Action.ROTATE)
                    elif event.key == pl.K_DOWN:
                        mod = 2
                    elif event.key == pl.K_LEFT:
                        game_screen.loop(GameScreen.Action.LEFT)
                    elif event.key == pl.K_RIGHT:
                        game_screen.loop(GameScreen.Action.RIGHT)
                    elif event.key == pl.K_SPACE:
                        game_screen.loop(GameScreen.Action.GROUND)
                if event.type == pl.KEYUP:
                    if event.key == pl.K_DOWN:
                        mod = 8
            if i % mod == 0:
                died = game_screen.loop(GameScreen.Action.STEP)
                i = 0
            pygame.display.update()
            if died:
                return 'foo'
            fps_clock.tick(FPS)
