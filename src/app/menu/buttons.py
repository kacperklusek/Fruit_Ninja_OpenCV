import pygame
from typing import Union
from pygame.math import Vector2
from src.app.utils.image_loader import ImageLoader


class FruitButton:
    def __init__(self, inner_image: str, outer_image: str, position: Vector2, size: Union[int, float] = 200):  # TODO - add type hints to every method
        self.original_inner_image = ImageLoader.load_png(inner_image, size * .35)
        self.original_outer_image = ImageLoader.load_png(outer_image, size)
        self.inner_image = self.original_inner_image
        self.outer_image = self.original_outer_image
        self.inner_width, self.inner_height = self.inner_image.get_size()
        self.outer_width, self.outer_height = self.outer_image.get_size()
        self.inner_angle = 0
        self.outer_angle = 0
        self.inner_rotation_speed = .2
        self.outer_rotation_speed = .05
        self.position = position

    @property
    def rect(self):
        rect = self.inner_image.get_rect()
        rect.x = self.position.x - self.inner_image.get_width() / 2
        rect.y = self.position.y - self.inner_image.get_height() / 2
        return rect

    def animate(self):
        # Rotate the inner image
        self.inner_angle = (self.inner_angle + self.inner_rotation_speed) % 360
        self.inner_image = pygame.transform.rotate(self.original_inner_image, self.inner_angle)

        # Rotate the outer image
        self.outer_angle = (self.outer_angle - self.outer_rotation_speed) % 360
        self.outer_image = pygame.transform.rotate(self.original_outer_image, self.outer_angle)

    def blit(self, surface):
        surface.blit(self.inner_image,
                    self.position - Vector2(self.inner_image.get_width() / 2, self.inner_image.get_height() / 2))

        # TODO - remove duplicated code
        surface.blit(self.outer_image,
                    self.position - Vector2(self.outer_image.get_width() / 2, self.outer_image.get_height() / 2))
