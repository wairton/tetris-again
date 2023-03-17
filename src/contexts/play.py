import sys

import pygame
import pygame.locals as pl

import json
import configuration.config as config
from mechanics import GameScreen
from .base import Context


class PlayContext(Context):

    def execute(self):
        STEP_REPEAT = pygame.USEREVENT
        LEFT_REPEAT = pygame.USEREVENT + 1
        RIGHT_REPEAT = pygame.USEREVENT + 2
        game_screen = GameScreen(self.drawer, (10, 60))
        FPS = 60  # frames per second setting
        SPF = 1000 // FPS
        fps_clock = pygame.time.Clock()
        try:
            options = json.load(open(config.OPTIONS_FILE))
        except Exception as e:
            print(e)
        get_key = pygame.key.key_code
        player1_options = options["Player1"]
        pygame.time.set_timer(STEP_REPEAT, SPF * 15)
        while True:
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
                    elif event.key == get_key(player1_options['Anti-Rotate']):
                        game_screen.loop(GameScreen.Action.ANTI_ROTATE)
                    elif event.key == get_key(player1_options['Down']):
                        pygame.time.set_timer(STEP_REPEAT, int(SPF * 3.75))
                    elif event.key == get_key(player1_options['Left']):
                        game_screen.loop(GameScreen.Action.LEFT)
                        pygame.time.set_timer(LEFT_REPEAT, 100)
                    elif event.key == get_key(player1_options['Right']):
                        game_screen.loop(GameScreen.Action.RIGHT)
                        pygame.time.set_timer(RIGHT_REPEAT, 100)
                    elif event.key == get_key(player1_options['Ground']):
                        died, score = game_screen.loop(GameScreen.Action.GROUND)
                        if died:
                            return score
                if event.type == pl.KEYUP:
                    if event.key == get_key(player1_options['Down']):
                        pygame.time.set_timer(STEP_REPEAT, SPF * 15)
                    elif event.key == get_key(player1_options['Left']):
                        pygame.time.set_timer(LEFT_REPEAT, 0)
                    elif event.key == get_key(player1_options['Right']):
                        pygame.time.set_timer(RIGHT_REPEAT, 0)
                if event.type == LEFT_REPEAT:
                    game_screen.loop(GameScreen.Action.LEFT)
                if event.type == RIGHT_REPEAT:
                    game_screen.loop(GameScreen.Action.RIGHT)
                if event.type == STEP_REPEAT:
                    died, score = game_screen.loop(GameScreen.Action.STEP)
                    if died:
                        return score
            pygame.display.update()
            fps_clock.tick(FPS)
