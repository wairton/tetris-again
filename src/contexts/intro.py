import time

import config
import color as cl
from .base import Context
from images import image_loader


class IntroContext(Context):
    def __init__(self, drawer):
        super().__init__(drawer)

    def execute(self):
        logo = image_loader(config.IMG_LOGO)
        self.drawer.fill(cl.BEAUTIFUL_BLUE)
        x, y = config.SCREEN_RESOUTION
        self.drawer.blit(logo.surface, ((x - logo.width) / 2, y / 3))
        self.drawer.display()
        time.sleep(2)
        self.drawer.fill(cl.BLACK)
        self.drawer.display()
        return 0
