import pygame
from pygame.math import Vector2
from enum import Enum
from ..item import Item


class FruitType(Enum):
    Apple = 0


class Fruit(Item):
    def __init__(self, fruit_type: FruitType, position: Vector2, velocity: Vector2 = Vector2(0, 0)):
        Item.__init__(self, position, velocity)
        self.image = self.load_image(fruit_type)

    @staticmethod
    def load_image(fruit_type: FruitType):
        path = ''

        pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
