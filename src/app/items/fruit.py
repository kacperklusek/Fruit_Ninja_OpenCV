from pygame.sprite import Group
from pygame.math import Vector2
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
    MAGIC_CONSTANT = .5  # THAT IS REALLY NECESSARY FOR FRUIT SLICING XD

    def __init__(self, image_path, group: Group):
        Item.__init__(self, image_path, group)

    def spawn(self, position: Vector2, velocity: Vector2 = Vector2(0, 0)):
        Item.spawn(self, position, velocity)

    def kill(self):
        Item.kill(self)
        if not self.item_out_of_bounds():
            self.spawn_slices()

    def spawn_slices(self):
        slice1 = SlicedFruit(slice_image_path(self.image_path, 1))
        slice2 = SlicedFruit(slice_image_path(self.image_path, 2))
        slice1.spawn(self.position, (self.velocity * self.MAGIC_CONSTANT))
        slice2.spawn(self.position, (self.velocity * self.MAGIC_CONSTANT))


class PlainFruit(Fruit):
    TYPE = ItemType.PLAIN_FRUIT

    def __init__(self, fruit_type: FruitType, group: Group):
        Fruit.__init__(self, fruit_image_path(fruit_type), group)


class SlicedFruit(Item):
    group = Group()

    def __init__(self, image: str):
        Item.__init__(self, image, self.group)

    def spawn(self, position: Vector2, velocity: Vector2 = Vector2(0, 0)):
        Item.spawn(self, position, velocity)

    def kill(self):
        Item.kill(self)




# TODO
class GravityFruit(Fruit):
    # TODO - add type

    def __init__(self):
        super().__init__(fruit_image_path('gravity-banana'))


class FreezeFruit(Fruit):
    # TODO - add type

    def __init__(self):
        super().__init__(fruit_image_path('freeze-banana'))
