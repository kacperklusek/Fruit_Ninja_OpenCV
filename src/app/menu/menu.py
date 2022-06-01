import pygame.display

from src.app.menu.buttons import FruitButton
from src.config import window_config, menu_config
from pygame.math import Vector2
from enum import Enum, auto


class MenuEnum(Enum):
    MAIN = auto()
    ORIGINAL = auto()
    MULTIPLAYER = auto()


class MainMenuInputEnum(Enum):
    ORIGINAL = auto()
    MULTIPLAYER = auto()


class OriginalMenuInputEnum(Enum):
    CLASSIC = auto()
    ARCADE = auto()
    ZEN = auto()


class MultiplayerMenuInputEnum(Enum):
    CLASSIC_ATTACK = auto()
    ZEN_DUEL = auto()


class Menu:
    QUIT_BUTTON_SIZE = window_config.WIDTH * .15

    def __init__(self, game):
        self.game = game
        self.blade = game.blade
        self.menu_surface = pygame.Surface((
            window_config.WIDTH - 2 * menu_config.PADDING,
            window_config.HEIGHT - 2 * menu_config.PADDING
        ), flags=pygame.SRCALPHA)
        self.menu_surface_position = (
            menu_config.PADDING,
            menu_config.PADDING
        )

        self.quit_button = FruitButton(
            menu_config.QUIT_INNER_IMAGE,
            menu_config.QUIT_OUTER_IMAGE,
            Vector2(
                self.menu_surface.get_width() - self.QUIT_BUTTON_SIZE / 2,
                self.menu_surface.get_height() - self.QUIT_BUTTON_SIZE / 2
            ),
            self.QUIT_BUTTON_SIZE
        )

        self.animated_elements = [self.quit_button]
        self.elements = [*self.animated_elements]
        self.run_display = True

    def add_animated_elements(self, *elements):
        self.animated_elements.extend(elements)
        self.add_elements(*elements)

    def add_elements(self, *elements):
        self.elements.extend(elements)

    def animate(self):
        for element in self.animated_elements:
            element.animate()

    def blit_elements(self):
        for element in self.elements:
            element.blit(self.menu_surface)

    def update_screen(self):
        self.game.surface.blit(self.game.background, (0, 0))
        self.game.screen.blit(self.game.surface, (0, 0))
        self.blit_elements()
        self.game.screen.blit(self.menu_surface, self.menu_surface_position)
        self.menu_surface.fill(pygame.Color(0, 0, 0, 0))
        self.game.blade.draw()
        pygame.display.update()

    def handle_input(self):
        if self.blade.collides(self.quit_button):
            self.game.exit()

    def display(self):
        self.run_display = True
        while self.run_display:
            self.game.handle_events()
            self.handle_input()
            self.animate()
            self.update_screen()


class MainMenu(Menu):
    ORIGINAL_BUTTON_SIZE = window_config.WIDTH * .3
    MULTIPLAYER_BUTTON_SIZE = window_config.WIDTH * .25

    def __init__(self, game):
        Menu.__init__(self, game)
        self.original_button = FruitButton(
            menu_config.ORIGINAL_INNER_IMAGE,
            menu_config.ORIGINAL_OUTER_IMAGE,
            Vector2(
                self.menu_surface.get_width() / 2,
                self.menu_surface.get_height() * .6
            ),
            self.ORIGINAL_BUTTON_SIZE
        )
        self.multiplayer_button = FruitButton(
            menu_config.MULTIPLAYER_INNER_IMAGE,
            menu_config.MULTIPLAYER_OUTER_IMAGE,
            Vector2(
                self.MULTIPLAYER_BUTTON_SIZE / 2,
                self.menu_surface.get_height() * .9 - self.MULTIPLAYER_BUTTON_SIZE / 2
            ),
            self.MULTIPLAYER_BUTTON_SIZE
        )
        self.add_animated_elements(self.original_button, self.multiplayer_button)

    def handle_input(self):
        Menu.handle_input(self)
        match self.get_input():
            case MainMenuInputEnum.ORIGINAL:
                self.game.display_menu(MenuEnum.ORIGINAL)
                self.run_display = False
            case MainMenuInputEnum.MULTIPLAYER:
                self.game.display_menu(MenuEnum.MULTIPLAYER)
                self.run_display = False

    def get_input(self):
        if self.game.blade.collides(self.original_button):
            return MainMenuInputEnum.ORIGINAL
        if self.game.blade.collides(self.multiplayer_button):
            return MainMenuInputEnum.MULTIPLAYER
        return None


class OriginalModeMenu(Menu):
    CLASSIC_BUTTON_SIZE = window_config.WIDTH * .25
    ARCADE_BUTTON_SIZE = window_config.WIDTH * .25
    ZEN_BUTTON_SIZE = window_config.WIDTH * .25

    def __init__(self, game):
        Menu.__init__(self, game)
        self.classic_button = FruitButton(
            menu_config.CLASSIC_INNER_IMAGE,
            menu_config.CLASSIC_OUTER_IMAGE,
            Vector2(
                self.menu_surface.get_width() * .05 + self.CLASSIC_BUTTON_SIZE / 2,
                self.menu_surface.get_height() * .55
            ),
            self.CLASSIC_BUTTON_SIZE
        )
        self.arcade_button = FruitButton(
            menu_config.ARCADE_INNER_IMAGE,
            menu_config.ARCADE_OUTER_IMAGE,
            Vector2(
                self.menu_surface.get_width() / 2,
                self.menu_surface.get_height() * .95 - self.ARCADE_BUTTON_SIZE / 2
            ),
            self.ARCADE_BUTTON_SIZE
        )
        self.zen_button = FruitButton(
            menu_config.ZEN_INNER_IMAGE,
            menu_config.ZEN_OUTER_IMAGE,
            Vector2(
                self.menu_surface.get_width() * .95 - self.ZEN_BUTTON_SIZE / 2,
                self.menu_surface.get_height() * .55
            ),
            self.ZEN_BUTTON_SIZE
        )
        self.add_animated_elements(self.classic_button, self.arcade_button, self.zen_button)

    def handle_input(self):
        Menu.handle_input(self)
        match self.get_input():
            case MainMenuInputEnum.ORIGINAL:
                pass  # TODO
            case MainMenuInputEnum.MULTIPLAYER:
                pass  # TODO

    def get_input(self):
        if self.game.blade.collides(self.classic_button):
            return OriginalMenuInputEnum.CLASSIC
        if self.game.blade.collides(self.arcade_button):
            return OriginalMenuInputEnum.ARCADE
        if self.game.blade.collides(self.zen_button):
            return OriginalMenuInputEnum.ZEN
        return None


class MultiplayerModeMenu(Menu):
    CLASSIC_ATTACK_BUTTON_SIZE = window_config.WIDTH * .25
    ZEN_DUEL_BUTTON_SIZE = window_config.WIDTH * .25

    def __init__(self, game):
        Menu.__init__(self, game)
        self.classic_attack_button = FruitButton(
            menu_config.CLASSIC_ATTACK_INNER_IMAGE,
            menu_config.CLASSIC_ATTACK_OUTER_IMAGE,
            Vector2(
                self.menu_surface.get_width() / 2 - self.CLASSIC_ATTACK_BUTTON_SIZE * .75,
                self.menu_surface.get_height() / 2
            ),
            self.CLASSIC_ATTACK_BUTTON_SIZE
        )
        self.zen_duel_button = FruitButton(
            menu_config.ZEN_DUEL_INNER_IMAGE,
            menu_config.ZEN_DUEL_OUTER_IMAGE,
            Vector2(
                self.menu_surface.get_width() / 2 + self.ZEN_DUEL_BUTTON_SIZE * .75,
                self.menu_surface.get_height() / 2
            ),
            self.ZEN_DUEL_BUTTON_SIZE
        )
        self.add_animated_elements(self.classic_attack_button, self.zen_duel_button)

    def handle_input(self):
        Menu.handle_input(self)
        match self.get_input():
            case MultiplayerMenuInputEnum.CLASSIC_ATTACK:
                pass  # TODO
            case MultiplayerMenuInputEnum.ZEN_DUEL:
                pass  # TODO

    def get_input(self):
        if self.game.blade.collides(self.classic_attack_button):
            return MultiplayerMenuInputEnum.CLASSIC_ATTACK
        if self.game.blade.collides(self.zen_duel_button):
            return MultiplayerMenuInputEnum.ZEN_DUEL
        return None
