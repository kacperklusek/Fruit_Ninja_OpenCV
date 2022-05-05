import os
import pygame
from pygame.math import Vector2

from src.app.items.item import Item


class Fruit(Item):
    group = pygame.sprite.Group()

    def __init__(self, image_path, position: Vector2, velocity: Vector2 = Vector2(0, 0)):
        Item.__init__(self, image_path, position, velocity)
        self.fruit_config = image_path
        self.group.add(self)

    def kill(self):
        self.group.remove(self)
        super().kill()


class PlainFruit(Fruit):
    def __init__(self, image_path, position: Vector2, velocity: Vector2 = Vector2(0, 0)):
        super().__init__(image_path, position, velocity)
