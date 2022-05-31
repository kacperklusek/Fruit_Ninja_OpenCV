import pygame
from src.app.helpers.point import Point
from src.config import MainMenuConfig


class Button:
    def __init__(self, inner_image: str, outer_image: str, position: Point):
        self.inner_image = pygame.image.load(inner_image).convert_alpha()
        self.outer_image = pygame.image.load(outer_image).convert_alpha()
        self.inner_width, self.inner_height = self.inner_image.get_size()
        self.outer_width, self.outer_height = self.outer_image.get_size()
        self.inner_angle = 0
        self.outer_angle = 0


class NewGameButton(Button):
    def __init__(self):
        Button.__init__(self)
