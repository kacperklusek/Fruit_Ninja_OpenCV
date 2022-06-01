import pygame
from pygame.math import Vector2
from pygame.color import Color
from typing import Union
from src.app.utils.enums import Orientation
from .common import MenuElement


class ProgressBar(MenuElement):
    def __init__(self,
                 width: Union[int, float],
                 height: Union[int, float],
                 orientation: Orientation,
                 position: Vector2,
                 color: Color):
        self.position = position
        self.width = width
        self.height = height
        self.orientation = orientation
        self.bar = pygame.Surface((width, height))
        self._bar_size = 0
        self._progress = 0

    @property
    def progress(self):
        return self.progress

    @progress.setter
    def progress(self, value: float):
        if not 0 <= value <= 1:
            raise ValueError('Progress must be between 0 and 1')
        self._progress = value

    def update(self):
        if self.orientation is Orientation.HORIZONTAL:
            self._bar_size = self._progress * self.width
            self.bar = pygame.transform.scale(self.bar, (self._bar_size, self.height))
        else:
            self._bar_size = self._progress * self.height
            self.bar = pygame.transform.scale(self.bar, (self.width, self._bar_size))

    def blit(self, surface):
        ...  # TODO
