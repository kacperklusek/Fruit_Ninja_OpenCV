import pygame
from pygame.math import Vector2
from src.config import main_menu_config


class Button:
    def __init__(self, inner_image: str, outer_image: str, position: Vector2):
        self.original_inner_image = pygame.image.load(inner_image).convert_alpha()
        self.original_outer_image = pygame.image.load(outer_image).convert_alpha()
        self.inner_image = self.original_inner_image
        self.outer_image = self.original_outer_image
        self.inner_width, self.inner_height = self.inner_image.get_size()
        self.outer_width, self.outer_height = self.outer_image.get_size()
        self.inner_angle = 0
        self.outer_angle = 0
        self.rotation_speed = 1
        self.position = position

    def update(self, screen):
        # Rotate the inner image
        self.inner_angle = (self.inner_angle + self.rotation_speed) % 360
        self.inner_image = pygame.transform.rotate(self.original_inner_image, self.inner_angle)
        inner_rect = self.inner_image.get_rect()
        inner_rect.x = self.position.x - self.inner_image.get_width() / 2
        inner_rect.y = self.position.y - self.inner_image.get_height() / 2
        screen.blit(self.inner_image, self.position)

        # TODO - remove duplicated code
        # Rotate the outer image
        self.outer_angle = (self.outer_angle - self.rotation_speed) % 360
        self.outer_image = pygame.transform.rotate(self.original_outer_image, self.outer_angle)
        outer_rect = self.outer_image.get_rect()
        outer_rect.x = self.position.x - self.outer_image.get_width() / 2
        outer_rect.y = self.position.y - self.outer_image.get_height() / 2
        screen.blit(self.outer_image, self.position)


class NewGameButton(Button):
    def __init__(self, position: Vector2):
        inner_image = main_menu_config.NEW_GAME_INNER_IMAGE
        outer_image = main_menu_config.NEW_GAME_OUTER_IMAGE
        Button.__init__(self, inner_image, outer_image, position)


class DojoButton(Button):  # TODO - add classic/arcade buttons
    def __init__(self, position: Vector2):
        inner_image = main_menu_config.DOJO_INNER_IMAGE
        outer_image = main_menu_config.DOJO_OUTER_IMAGE
        Button.__init__(self, inner_image, outer_image, position)


class QuitButton(Button):
    def __init__(self, position: Vector2):
        inner_image = main_menu_config.QUIT_INNER_IMAGE
        outer_image = main_menu_config.QUIT_OUTER_IMAGE
        Button.__init__(self, inner_image, outer_image, position)
