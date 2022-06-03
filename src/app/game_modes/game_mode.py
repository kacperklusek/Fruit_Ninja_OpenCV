import pygame
from pygame import Surface
from pygame.color import Color
from pygame.sprite import Group

from abc import ABC, abstractmethod
from src.app.controllers.time_controller import TimeController
from src.app.effects.sounds import SoundController
from src.app.effects.visual import Trail
from src.config import window_config, effects_config


class GameModeCommon(ABC):
    EMPTY_COLOR = Color(0, 0, 0, 0)

    def __init__(self, game):
        self.game = game
        self.time_controller = TimeController()

        self.effects_surface = Surface((
            window_config.WIDTH,
            window_config.HEIGHT
        ), pygame.SRCALPHA)
        self.hud_surface = Surface((
            window_config.WIDTH,
            window_config.HEIGHT
        ), pygame.SRCALPHA)
        self.combo_surface = Surface((
            window_config.WIDTH,
            window_config.HEIGHT
        ), pygame.SRCALPHA)

        self.effects = Group()
        self.combo = Group()
        self.hud_elements = []

    def notify_item_spawn(self, item):
        if effects_config.DISPLAY_ITEM_TRAIL:
            Trail(item, self.effects)

    def update(self):
        self.hud_surface.fill(self.EMPTY_COLOR)
        self.combo_surface.fill(self.EMPTY_COLOR)
        self.effects_surface.fill(self.EMPTY_COLOR)

        self.effects.update(surface=self.effects_surface)
        self.combo.update()

        self.effects.draw(self.effects_surface)
        self.combo.draw(self.combo_surface)

        for hud_element in self.hud_elements:
            hud_element.blit(self.hud_surface)

        self.game.screen.blit(self.effects_surface, (0, 0))
        self.game.screen.blit(self.combo_surface, (0, 0))
        self.game.screen.blit(self.hud_surface, (0, 0))

    def handle_fruit_collision(self, fruit):
        SoundController.play_splatter_sound()
        fruit.slice(self.effects)
        fruit.kill()

    def _spawn_fruit_slices(self, fruit):
        pass

    @abstractmethod
    def handle_out_of_bounds(self):
        pass

    @abstractmethod
    def handle_collisions(self):
        pass

    @abstractmethod
    def blit_items(self):
        pass
