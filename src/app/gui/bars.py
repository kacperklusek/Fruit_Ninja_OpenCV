import pygame
from typing import Union
from pygame import Surface
from pygame.font import Font
from pygame.color import Color
from pygame.math import Vector2
from src.app.gui.common import MenuElement
from src.app.utils.enums import Orientation
from src.app.utils.image_loader import ImageLoader
from src.app.controllers.score_controller import ScoreController
from src.config import health_bar_config, window_config, game_config, menu_config


class ProgressBar(MenuElement):
    BORDER_RADIUS = 10

    def __init__(self,
                 width: Union[int, float],
                 height: Union[int, float],
                 orientation: Orientation,
                 position: Vector2,
                 color: Color):
        self.position = position
        self.width = width
        self.height = height
        self.color = color
        self.orientation = orientation
        self.bar = Surface((width, height))
        self._bar_size = 0
        self._progress = 0

    @property
    def progress(self):
        return self.progress

    def update(self, progress: float):
        if not 0 <= progress <= 1:
            raise ValueError('Progress must be between 0 and 1')
        self._progress = progress

        if self.orientation is Orientation.HORIZONTAL:
            self._bar_size = self._progress * self.width
            self.bar = pygame.transform.scale(self.bar, (self._bar_size, self.height))
        else:
            self._bar_size = self._progress * self.height
            self.bar = pygame.transform.scale(self.bar, (self.width, self._bar_size))

    def blit(self, surface):
        pygame.draw.rect(surface, self.color, self.bar.get_rect(topleft=self.position), 0, self.BORDER_RADIUS)


class HealthIcon(MenuElement):
    def __init__(self, inner_image_path: str, outer_image_path: str, position: Vector2):
        self.inner_image = ImageLoader.load_png(inner_image_path)
        self.outer_image = ImageLoader.load_png(outer_image_path)
        self.position = position
        self.lost = False

    def blit(self, surface):
        surface.blit(self.outer_image, self.position)
        if self.lost:
            surface.blit(self.inner_image, self.position)


class HealthBar(MenuElement):
    ICON_WIDTH = window_config.WIDTH * .1
    ICON_PADDING = -window_config.WIDTH * .05

    def __init__(self, max_lives):
        self.health_icons = self.__create_health_icons(max_lives)
        self._max_lives = max_lives
        self._lives = max_lives

    @property
    def lives(self):
        return self._lives

    def update_lives(self, lives):
        if not 0 <= lives <= self._max_lives:
            raise ValueError(f'Number of lives must be between 0 and {self._max_lives}')
        self._lives = lives
        self.update()

    def blit(self, surface):
        self.update()
        for icon in self.health_icons:
            icon.blit(surface)

    def update(self):
        for i, icon in enumerate(self.health_icons):
            icon.lost = i >= self.lives

    def __create_health_icons(self, lives):
        return [
            HealthIcon(
                health_bar_config.GET_HEALTH_ICON(i % health_bar_config.HEALTHS_COUNT + 1),
                health_bar_config.GET_FAILED_HEALTH_ICON(i % health_bar_config.HEALTHS_COUNT + 1),
                Vector2(
                    window_config.WIDTH - (lives - i) * (self.ICON_WIDTH + self.ICON_PADDING) - menu_config.PADDING,
                    menu_config.PADDING
                )
            )
            for i in range(lives)
        ]


class ScoreBar(MenuElement):
    SCORE_POSITION = Vector2(menu_config.PADDING, menu_config.PADDING)

    def __init__(self, score_controller: ScoreController):
        self.score = 0
        self.font = Font(game_config.FONT, game_config.FONT_SIZE)
        self.score_controller = score_controller
        self.score_controller.add_observer(self)

    def blit(self, surface):
        surface.blit(
            self.font.render(f'Your Score: {self.score}', True, 'White'),
            self.SCORE_POSITION)

    def update_score(self, score):
        self.score = score


class TimeBar(MenuElement):
    TIME_POSITION = Vector2(window_config.WIDTH - menu_config.PADDING, menu_config.PADDING)

    def __init__(self, time):
        self.total_time = time
        self.time_left = time
        self.font = Font(game_config.FONT, game_config.FONT_SIZE)

    def blit(self, surface):
        text = self.font.render(
            f'Time left: {self.time_left//60}:{"0" if self.time_left%60 < 10 else ""}{self.time_left%60}',
            True, 'White')
        surface.blit(
            text, self.TIME_POSITION - Vector2(text.get_width(), 0))

    def update_time(self, elapsed_time):
        self.time_left = int(self.total_time - elapsed_time)
