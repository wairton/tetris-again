import configuration.config as config

from .interfaces import Image


def image_loader(path) -> Image:
    if config.BACKEND == config.Backend.PYGAME:
        from .pygame import PygameImage
        return PygameImage(path)
    else:
        raise ValueError("not implemented yet")


__all__ = [image_loader, Image]
