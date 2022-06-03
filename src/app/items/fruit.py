import math
from pygame.sprite import Group
from pygame.math import Vector2

from src.app.effects.visual import Trail
from src.config import image_path

from src.app.items.item import Item
from src.app.utils.enums import FruitType, ItemType


def fruit_image_path(fruit_name):
    return image_path('items', 'fruits', f'{fruit_name}.png')


def slice_image_path(image_path: str, slice_no: int):
    path = image_path.split('.')
    path[0] += f"-{slice_no}"
    return '.'.join(path)


class Fruit(Item):
    SLICE_RECOIL = 100

    def __init__(self, image_path, group: Group):
        Item.__init__(self, image_path, group)

    def slice(self, effects_group: Group, display_trail: bool = False):
        slice1 = FruitSlice(slice_image_path(self.image_path, 1), effects_group)
        slice2 = FruitSlice(slice_image_path(self.image_path, 2), effects_group)

        recoil_vector = self.SLICE_RECOIL * Vector2(math.cos(self.angle), math.sin(self.angle))
        slice1.throw(self.position - Vector2(1, 0), self.velocity - recoil_vector, self.angle, self.angular_velocity)
        slice2.throw(self.position + Vector2(1, 0), self.velocity + recoil_vector, self.angle, self.angular_velocity)

        if display_trail:
            Trail(slice1, effects_group, min(slice1.height, slice1.width) / 5)
            Trail(slice2, effects_group, min(slice2.height, slice2.width) / 5)


class PlainFruit(Fruit):
    TYPE = ItemType.PLAIN_FRUIT

    def __init__(self, fruit_type: FruitType, group: Group):
        Fruit.__init__(self, fruit_image_path(fruit_type), group)


class FruitSlice(Item):
    def __init__(self, image_path: str, group: Group):
        Item.__init__(self, image_path, group)


class GravityFruit(Fruit):
    TYPE = ItemType.BONUS_FRUIT

    def __init__(self, group):
        super().__init__(fruit_image_path('gravity-banana'), group)


class FreezeFruit(Fruit):
    TYPE = ItemType.BONUS_FRUIT

    def __init__(self, group):
        super().__init__(fruit_image_path('freeze-banana'), group)
