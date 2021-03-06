from pygame.sprite import Group
from src.config import image_path
from src.app.items.item import Item
from src.app.utils.enums import ItemType


class Bomb(Item):
    TYPE = ItemType.BOMB
    IMG_PATH = image_path('items', 'bombs', 'bomb.png')

    def __init__(self, group: Group):
        Item.__init__(self, self.IMG_PATH, group)
