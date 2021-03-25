from abc import ABC, abstractmethod


class Image(ABC):
    def __init__(self, path):
        self._image = self.load(path)


    @property
    @abstractmethod
    def surface(self):
        pass

    @property
    @abstractmethod
    def width(self):
        pass

    @property
    @abstractmethod
    def size(self):
        pass

    @abstractmethod
    def load(self, path):
        pass
