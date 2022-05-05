import pygame
from src.app.items.item import Item
from src.config import image_path


class Bomb(Item):
    IMG_PATH = image_path('items', 'bombs', 'bomb.png')

    group = pygame.sprite.Group()

    def __init__(self):
        Item.__init__(self, self.IMG_PATH)
        self.group.add(self)

    def kill(self):
        self.group.remove(self)
        super().kill()

    def handle_out_of_bounds(self):
        self.kill()
