import os
import pygame
from pygame.math import Vector2
from src.app.items.item import Item


class Bomb(Item):
    IMG_PATH = os.path.join('assets', 'images', 'items', 'bombs', 'Bomb.png')

    group = pygame.sprite.Group()

    def __init__(self, position: Vector2, velocity: Vector2 = Vector2(0, 0)):
        Item.__init__(self, self.IMG_PATH, position, velocity)
        self.group.add(self)

    def kill(self):
        self.group.remove(self)
        super().kill()

    def handle_out_of_bounds(self):
        self.kill()

