import time
import pygame
from typing import Union
from pygame.color import Color
from abc import abstractmethod
from pygame.math import Vector2
from src.app.gui.bars import ProgressBar
from src.app.utils.enums import Orientation
from src.app.utils.image_loader import ImageLoader
from src.app.controllers.input_controller import MouseInput
from src.app.gui.common import MenuElement, AnimatedMenuElement


class Button(MenuElement):
    def __init__(self, game):
        self.game = game

    @property
    def checked(self):
        return self.game.blade.collides(self)

    @property
    @abstractmethod
    def rect(self):
        pass

    @property
    @abstractmethod
    def width(self):
        pass

    @property
    @abstractmethod
    def height(self):
        pass


class TimedButton(Button):
    PROGRESS_BAR_WIDTH_RATIO = .95
    PROGRESS_BAR_HEIGHT_RATIO = .1

    def __init__(self,
                 game,
                 image_path: str,
                 position: Vector2,
                 progress_bar_color: Color,
                 hover_duration: Union[int, float] = 2,
                 hover_stop_tolerance: Union[int, float] = .25,
                 width: Union[int, float] = -1,
                 height: Union[int, float] = -1):
        Button.__init__(self, game)
        self.image = ImageLoader.load_png(image_path, width, height)
        self.hover_duration = hover_duration
        self.hover_stop_tolerance = hover_stop_tolerance
        self.position = position
        self.hover_start_time = float('inf')
        self.hover_stop_time = float('inf')
        self.is_hovering = False

        self.progress_bar = ProgressBar(
            self.PROGRESS_BAR_WIDTH_RATIO * width,
            max(self.PROGRESS_BAR_HEIGHT_RATIO * height, 1),
            Orientation.HORIZONTAL,
            position + Vector2(((1 - self.PROGRESS_BAR_WIDTH_RATIO) * self.width) / 2, .1 * self.height),
            progress_bar_color
        )

    @property
    def checked(self):
        # Do not apply timeout while using the MouseInput controller
        if isinstance(self.game.blade.input_source, MouseInput):
            return self.game.blade.collides(self)

        curr_time = time.time()
        if not self.game.blade.collides(self):
            if curr_time - self.hover_stop_time > self.hover_stop_tolerance:
                self.reset()
            elif self.hover_stop_time == float('inf'):
                self.hover_stop_time = curr_time
            return False

        self.hover_stop_time = float('inf')
        if not self.is_hovering:
            self.is_hovering = True
            self.hover_start_time = curr_time

        return curr_time - self.hover_start_time >= self.hover_duration

    @property
    def rect(self):
        return self.image.get_rect(topleft=self.position + Vector2(self.height / 2, self.height / 2))

    @property
    def width(self):
        return self.image.get_width()

    @property
    def height(self):
        return self.image.get_height()

    def blit(self, surface):
        surface.blit(self.image, self.position)

        if self.is_hovering:
            progress = min(max((time.time() - self.hover_start_time) / self.hover_duration, 0), 1)
            self.progress_bar.update(progress)
            self.progress_bar.blit(surface)

    def reset(self):
        self.is_hovering = False
        self.hover_start_time = float('inf')
        self.hover_stop_time = float('inf')


class FruitButton(Button, AnimatedMenuElement):
    def __init__(self,
                 blade,
                 inner_image_path: str,
                 outer_image_path: str,
                 position: Vector2,
                 size: Union[int, float] = -1,
                 inner_rotation_speed: Union[int, float] = .2,
                 outer_rotation_speed: Union[int, float] = -.05,
                 inner_initial_angle: Union[int, float] = 0,
                 outer_initial_angle: Union[int, float] = 0):
        Button.__init__(self, blade)
        self.original_inner_image = ImageLoader.load_png(inner_image_path, size * .35)
        self.original_outer_image = ImageLoader.load_png(outer_image_path, size)
        self.inner_image = self.original_inner_image
        self.outer_image = self.original_outer_image
        self.inner_current_angle = inner_initial_angle
        self.outer_current_angle = outer_initial_angle
        self.inner_rotation_speed = inner_rotation_speed
        self.outer_rotation_speed = outer_rotation_speed
        self.position = position
        self.scale = 1
        self.alpha = 255

    @property
    def rect(self):
        return self.outer_image.get_rect(center=self.position)

    @property
    def width(self):
        return self.outer_image.get_width()

    @property
    def height(self):
        return self.outer_image.get_height()

    def animate(self):
        # Rotate the inner image
        self.inner_image, self.inner_current_angle = self.rotate(
            self.original_inner_image, self.inner_current_angle, self.inner_rotation_speed
        )
        # Rotate the outer image
        self.outer_image, self.outer_current_angle = self.rotate(
            self.original_outer_image, self.outer_current_angle, self.outer_rotation_speed
        )

    @staticmethod
    def rotate(image, curr_angle, rotation_speed):
        new_angle = (curr_angle + rotation_speed) % 360
        return pygame.transform.rotate(image, new_angle), new_angle

    def blit(self, surface):
        inner_image_scale = (self.scale * self.inner_image.get_width(), self.scale * self.inner_image.get_height())
        outer_image_scale = (self.scale * self.width, self.scale * self.height)
        inner_image = pygame.transform.scale(self.inner_image, inner_image_scale)
        outer_image = pygame.transform.scale(self.outer_image, outer_image_scale)
        inner_image.set_alpha(self.alpha)
        outer_image.set_alpha(self.alpha)
        self._blit_centered(inner_image, surface)
        self._blit_centered(outer_image, surface)

    def _blit_centered(self, image, surface):
        surface.blit(image, self.position - Vector2(image.get_width() / 2, image.get_height() / 2))
