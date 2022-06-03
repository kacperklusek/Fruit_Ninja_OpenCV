import pygame
from pygame import Surface
from pygame.color import Color
from pygame.sprite import Group
from abc import ABC, abstractmethod
from src.app.effects.visual import Trail
from src.app.effects.sounds import SoundController
from src.config import window_config, effects_config
from src.app.controllers.time_controller import TimeController


class GameModeCommon(ABC):
    EMPTY_COLOR = Color(0, 0, 0, 0)

    def __init__(self, game):
        self.game = game
        self.time_controller = TimeController()

        self.effects_surface = self._create_surface()
        self.fruit_slices_surface = self._create_surface()
        self.hud_surface = self._create_surface()
        self.labels_surface = self._create_surface()

        self.fruit_slices = Group()
        self.effects = Group()
        self.labels = Group()
        self.hud_elements = []

    def notify_item_spawn(self, item):
        if effects_config.DISPLAY_ITEM_TRAIL:
            Trail(item, self.effects)

    def update(self):
        self.hud_surface.fill(self.EMPTY_COLOR)
        self.labels_surface.fill(self.EMPTY_COLOR)
        self.effects_surface.fill(self.EMPTY_COLOR)
        self.fruit_slices_surface.fill(self.EMPTY_COLOR)

        self.effects.update(surface=self.effects_surface)
        self.fruit_slices.update()
        self.labels.update()

        self.fruit_slices.draw(self.fruit_slices_surface)
        self.effects.draw(self.effects_surface)
        self.labels.draw(self.labels_surface)

        for hud_element in self.hud_elements:
            hud_element.blit(self.hud_surface)

        self.game.screen.blit(self.effects_surface, (0, 0))
        self.game.screen.blit(self.fruit_slices_surface, (0, 0))
        self.game.screen.blit(self.labels_surface, (0, 0))
        self.game.screen.blit(self.hud_surface, (0, 0))

    def handle_fruit_collision(self, fruit):
        SoundController.play_splatter_sound()
        fruit.slice(self.fruit_slices, self.effects)
        fruit.kill()

    def clear(self):
        for fruit_slice in self.fruit_slices:
            fruit_slice.kill()

    def _spawn_fruit_slices(self, fruit):
        pass

    @staticmethod
    def _create_surface():
        return Surface((
            window_config.WIDTH,
            window_config.HEIGHT
        ), pygame.SRCALPHA)

    @abstractmethod
    def handle_out_of_bounds(self):
        pass

    @abstractmethod
    def handle_collisions(self):
        pass

    @abstractmethod
    def blit_items(self):
        pass

    @abstractmethod
    def start_game(self):
        pass
