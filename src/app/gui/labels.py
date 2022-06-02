from pygame import Vector2
from pygame.surface import SurfaceType, Surface


class ScoreLabel:
    def __init__(self, text: Surface | SurfaceType, position: Vector2):
        self.text = text
        self.position = position

    @property
    def rect(self):
        rect = self.text.get_rect()
        rect.y = self.position.y
        rect.x = self.position.x
        return rect

    def blit(self, surface):
        surface.blit(self.text, self.position)
