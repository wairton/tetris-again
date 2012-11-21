import pygame

class Draw(object):
    def __init__(self, surface=None):
        self._surface = surface
                
    @property
    def surface(self):
        return self._surface
    
    @surface.setter
    def surface(self, surface):
        self._surface = surface

    def display(self):
        pygame.display.update()
        
    def blit(self, *args):
        self.surface.blit(*args)
        
    def fill(self, *args):
        self.surface.fill(*args)
        
    def line(self, *args):
        pygame.draw.line(self.surface, *args)
    
    def circle(self, *args):
        pygame.draw.circle(self.surface, *args)
        
    def ellipse(self, *args):
        pygame.draw.ellipse(self.surface, *args)
        
    def rect(self, *args):
        pygame.draw.rect(self.surface, *args)
        
    def polygon(self, *args):
        pygame.draw.polygon(self.surface, *args)
