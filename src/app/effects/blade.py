# from typing import Any

import pygame
from pygame.math import Vector2


# from src.game import WIDTH, HEIGHT


class Blade(pygame.sprite.Sprite):  # TODO - replace line drawing from main with instance of this class
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.mask = None
        # self.image = pygame.Surface((800, 400))
        # self.image.set_colorkey((0, 0, 0))
        # self.rect = self.image.get_rect(center=(0, 0))
        self.start = Vector2(0, 0)
        self.end = Vector2(0, 0)

    def update(self, start, end) -> None:
        self.start = start
        self.end = end
        pygame.draw.line(self.image, 'White', start, end, 5)
        # self.mask = pygame.mask.from_surface(self.image)
        # self.mask = pygame.mask
