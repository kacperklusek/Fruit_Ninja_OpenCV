import pygame
from pygame.math import Vector2
from src.config import image_path

from src.app.items.item import Item
from src.app.utils.enums import PlainFruitType


def fruit_image_path(fruit_name):
    return image_path('items', 'fruits', f'{fruit_name}.png')


def slice_image_path(img_path: str, slice_no: int):
    path = img_path.split('.')
    path[0] += f"-{slice_no}"
    return '.'.join(path)


class Fruit(Item):
    MAGIC_CONSTANT = .5 # THAT IS REALLY NECESSARY FOR FRUIT SLICING XD
    group = pygame.sprite.Group()

    def __init__(self, image):
        Item.__init__(self, image)

    def spawn(self, position: Vector2, velocity: Vector2 = Vector2(0, 0)):
        self.group.add(self)
        super().spawn(position, velocity)

    def kill(self):
        if not self.item_out_of_bounds():
            self.spawn_slices()

        self.group.remove(self)
        super().kill()

    def spawn_slices(self):
        if "banana" in self.img_path:
            return

        slice1 = SlicedFruit(slice_image_path(self.img_path, 1))
        slice2 = SlicedFruit(slice_image_path(self.img_path, 2))
        slice1.spawn(self.position, self.velocity * self.MAGIC_CONSTANT)
        slice2.spawn(self.position, self.velocity * self.MAGIC_CONSTANT)


class PlainFruit(Fruit):
    def __init__(self, fruit_type: PlainFruitType):
        super().__init__(fruit_image_path(fruit_type))


class GravityFruit(Fruit):
    def __init__(self):
        super().__init__(fruit_image_path('gravity-banana'))


class FreezeFruit(Fruit):
    def __init__(self):
        super().__init__(fruit_image_path('freeze-banana'))


class SlicedFruit(Fruit):
    group = pygame.sprite.Group()

    def __init__(self, image: str):
        Item.__init__(self, image)

    def spawn(self, position: Vector2, velocity: Vector2 = Vector2(0, 0)):
        self.group.add(self)
        super().spawn(position, velocity)

    def handle_out_of_bounds(self):
        self.group.remove(self)
