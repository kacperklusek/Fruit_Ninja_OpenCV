from pygame.sprite import Group
from pygame.math import Vector2
from src.app.items.item import Item
from src.app.utils.enums import ItemType
from src.config import image_path


class Bomb(Item):
    TYPE = ItemType.BOMB

    IMG_PATH = image_path('items', 'bombs', 'bomb.png')

    def __init__(self, group: Group):
        Item.__init__(self, self.IMG_PATH, group)

    def spawn(self, position: Vector2, velocity: Vector2 = Vector2(0, 0)):
        Item.spawn(self, position, velocity)

    def handle_out_of_bounds(self):
        self.kill()
