import pygame
from pygame.math import Vector2
from pygame.color import Color
from typing import Union
from src.app.utils.enums import Orientation
from .common import MenuElement


class ProgressBar(MenuElement):
    BORDER_RADIUS = 10

    def __init__(self,
                 width: Union[int, float],
                 height: Union[int, float],
                 orientation: Orientation,
                 position: Vector2,
                 color: Color):
        self.position = position
        self.width = width
        self.height = height
        self.color = color
        self.orientation = orientation
        self.bar = pygame.Surface((width, height))
        self._bar_size = 0
        self._progress = 0

    @property
    def progress(self):
        return self.progress

    def update(self, progress: float):
        if not 0 <= progress <= 1:
            raise ValueError('Progress must be between 0 and 1')
        self._progress = progress

        if self.orientation is Orientation.HORIZONTAL:
            self._bar_size = self._progress * self.width
            self.bar = pygame.transform.scale(self.bar, (self._bar_size, self.height))
        else:
            self._bar_size = self._progress * self.height
            self.bar = pygame.transform.scale(self.bar, (self.width, self._bar_size))

    def blit(self, surface):
        pygame.draw.rect(surface, self.color, self.bar.get_rect(topleft=self.position), 0, self.BORDER_RADIUS)
