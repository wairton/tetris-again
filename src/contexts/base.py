from abc import ABC, abstractmethod


class Context(ABC):
    def __init__(self, drawer):
        self.drawer = drawer

    @abstractmethod
    def execute(self):
        pass
