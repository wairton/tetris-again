import time

import config
import color
from images import image_loader
from .base import Context


class IntroContext(Context):
    def execute(self):
        logo = image_loader(config.IMG_LOGO)
        self.drawer.fill(color.BEAUTIFUL_BLUE)
        x, y = config.SCREEN_RESOUTION
        self.drawer.blit(logo.surface, ((x - logo.width) / 2, y / 3))
        self.drawer.display()
        time.sleep(2)
        self.drawer.fill(color.BLACK)
        self.drawer.display()
        return 0
