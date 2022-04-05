import os
import pygame
from pygame.math import Vector2
from enum import Enum
from ..item import Item


class FruitType(Enum):
    Apple = 'Apple'
    Orange = 'Orange'
    Banana = 'Banana'


class Fruit(Item):
    APPLE_IMG_PATH = os.path.join('assets', 'images', 'items', 'fruits', 'apple.png')

    group = pygame.sprite.Group()

    def __init__(self, fruit_type: FruitType, position: Vector2, velocity: Vector2 = Vector2(0, 0)):
        Item.__init__(self, self.get_image_path(fruit_type), position, velocity)
        self.group.add(self)

    def kill(self):
        self.group.remove(self)
        super().kill()

    @classmethod
    def get_image_path(cls, fruit_type: FruitType):
        return cls.APPLE_IMG_PATH
