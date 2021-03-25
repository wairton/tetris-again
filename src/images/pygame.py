import pygame

from .interfaces import Image


class PygameImage(Image):
    @property
    def surface(self):
        return self._image

    @property
    def width(self):
        return self._image.get_width()

    @property
    def size(self):
        return self._image.get_size()

    def load(self, path):
        return pygame.image.load(path)
