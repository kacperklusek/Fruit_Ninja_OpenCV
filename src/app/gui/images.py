import pygame

from .common import MenuElement
from pygame.math import Vector2
from src.app.utils.image_loader import ImageLoader


class Image(MenuElement):
    def __init__(self, image_path: str, position: Vector2, width: int = -1, height: int = -1):
        self.image = ImageLoader.load_png(image_path, width, height)
        self.position = position
        self.scale = 1
        self.alpha = 255

    def blit(self, surface):
        image = pygame.transform.scale(self.image, (self.scale * self.width, self.scale * self.height))
        image.set_alpha(self.alpha)
        surface.blit(image, self.position)

    @property
    def width(self):
        return self.image.get_width()

    @property
    def height(self):
        return self.image.get_height()
