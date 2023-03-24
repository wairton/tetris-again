import sys

import pygame
import pygame.locals as pl

import json
import configuration.config as config
from mechanics import GameScreen
from .base import Context


class PlayContext(Context):

    def execute(self):
        game_screen = GameScreen(self.drawer, (10, 60))
        i, mod = 0, 8
        FPS = 32  # frames per second setting
        died = False
        fps_clock = pygame.time.Clock()
        try:
            options = json.load(open(config.OPTIONS_FILE))
        except Exception as e:
            print(e)
        get_key = pygame.key.key_code
        player1_options = options["Player1"]
        while True:
            i += 1
            for event in pygame.event.get():
                if event.type == pl.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pl.KEYDOWN:
                    if event.key == pl.K_ESCAPE:
                        died, score = game_screen.loop(GameScreen.Action.STEP)
                        if score is None:
                            return 0
                        return score
                    elif event.key == get_key(player1_options['Rotate']):
                        game_screen.loop(GameScreen.Action.ROTATE)
                    elif event.key == get_key(player1_options['Down']):
                        mod = 2
                    elif event.key == get_key(player1_options['Left']):
                        game_screen.loop(GameScreen.Action.LEFT)
                    elif event.key == get_key(player1_options['Right']):
                        game_screen.loop(GameScreen.Action.RIGHT)
                    elif event.key == pl.K_h:
                        game_screen.loop(GameScreen.Action.HOLD)
                    elif event.key == get_key(player1_options['Ground']):
                        died, score = game_screen.loop(GameScreen.Action.GROUND)
                        if died:
                            return score
                if event.type == pl.KEYUP:
                    if event.key == get_key(player1_options['Down']):
                        mod = 8
            if i % mod == 0:
                died, score = game_screen.loop(GameScreen.Action.STEP)
                i = 0
            pygame.display.update()
            if died:
                return score
            fps_clock.tick(FPS)
