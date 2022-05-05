import os
import pygame
from pygame.math import Vector2

from src.app.items.item import Item


class Fruit(Item):
    group = pygame.sprite.Group()

    def __init__(self, fruit_config, position: Vector2, velocity: Vector2 = Vector2(0, 0)):
        Item.__init__(self, fruit_config.IMAGE_PATH, position, velocity)
        self.fruit_config = fruit_config
        self.group.add(self)

    def kill(self):
        self.group.remove(self)
        super().kill()
