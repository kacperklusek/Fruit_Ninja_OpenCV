import pygame
from pygame.math import Vector2
from src.config import image_path

from src.app.items.item import Item
from src.app.utils.enums.items import PlainFruitType


class Fruit(Item):
    group = pygame.sprite.Group()

    def __init__(self, fruit_type):
        image = image_path('items', 'fruits', f'{fruit_type}.png')
        Item.__init__(self, image)

    def spawn(self, position: Vector2, velocity: Vector2 = Vector2(0, 0)):
        self.group.add(self)
        super().spawn(position, velocity)

    def kill(self):
        self.group.remove(self)
        super().kill()


class PlainFruit(Fruit):
    def __init__(self, fruit_type: PlainFruitType):
        super().__init__(fruit_type)
