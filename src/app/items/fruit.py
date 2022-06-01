import pygame
from pygame.math import Vector2
from src.config import image_path

from src.app.items.item import Item
from src.app.utils.enums import PlainFruitType


def fruit_image_path(fruit_name):
    return image_path('items', 'fruits', f'{fruit_name}.png')


class Fruit(Item):
    group = pygame.sprite.Group()

    def __init__(self, image):
        Item.__init__(self, image)

    def spawn(self, position: Vector2, velocity: Vector2 = Vector2(0, 0)):
        self.group.add(self)
        super().spawn(position, velocity)

    def kill(self):
        self.group.remove(self)
        super().kill()


class PlainFruit(Fruit):
    def __init__(self, fruit_type: PlainFruitType):
        super().__init__(fruit_image_path(fruit_type))


class GravityFruit(Fruit):
    def __init__(self):
        super().__init__(fruit_image_path('gravity-banana'))


class FreezeFruit(Fruit):
    def __init__(self):
        super().__init__(fruit_image_path('freeze-banana'))
