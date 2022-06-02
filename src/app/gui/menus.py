import pygame.display
from pygame.font import Font

from src.app.gui.buttons import TimedButton, FruitButton
from src.app.gui.images import Image
from src.app.gui.labels import ScoreLabel
from src.config import window_config, menu_config, game_config
from pygame.math import Vector2
from pygame.color import Color
from enum import Enum, auto
from .common import MenuElement
from ..game_modes.singleplayer.arcade_mode import ArcadeMode
from ..game_modes.singleplayer.classic_mode import ClassicMode
from ..game_modes.singleplayer.zen_mode import ZenMode
from ..utils.enums import GameMode


class MenuInput(Enum):
    MAIN = auto()
    ORIGINAL = auto()
    MULTIPLAYER = auto()
    GAME_OVER = auto()
    SINGLE_PLAYER_GAME_OVER_MENU = auto()
    MULTI_PLAYER_GAME_OVER_MENU = auto()


class MainMenuInput(Enum):
    ORIGINAL = auto()
    MULTIPLAYER = auto()


class OriginalMenuInput(Enum):
    BACK = auto()
    CLASSIC = auto()
    ARCADE = auto()
    ZEN = auto()


class MultiplayerMenuInput(Enum):
    BACK = auto()
    CLASSIC_ATTACK = auto()
    ZEN_DUEL = auto()


class GameOverMenuInputEnum(Enum):
    BACK = auto()


def create_back_button(game, menu_surface):
    back_button_width = window_config.WIDTH * .2
    back_button_height = .25 * back_button_width

    return TimedButton(
        game,
        menu_config.BACK_BUTTON_IMAGE,
        Vector2(
            menu_config.BACK_BUTTON_HOVER_DURATION,
            menu_surface.get_height() - back_button_height
        ),
        Color(255, 255, 255),
        menu_config.BACK_BUTTON_HOVER_DURATION,
        menu_config.HOVER_STOP_TOLERANCE,
        back_button_width,
        back_button_height,
    )


class Menu:
    QUIT_BUTTON_SIZE = window_config.WIDTH * .15

    def __init__(self, game):
        self.game = game
        self.blade = game.blade
        self.font = Font(game_config.FONT, game_config.FONT_SIZE)

        self.menu_surface = pygame.Surface((
            window_config.WIDTH - 2 * menu_config.PADDING,
            window_config.HEIGHT - 2 * menu_config.PADDING
        ), flags=pygame.SRCALPHA)
        self.menu_surface_position = (
            menu_config.PADDING,
            menu_config.PADDING
        )

        self.quit_button = FruitButton(
            game,
            menu_config.QUIT_INNER_IMAGE,
            menu_config.QUIT_OUTER_IMAGE,
            Vector2(
                self.menu_surface.get_width() - self.QUIT_BUTTON_SIZE / 2,
                self.menu_surface.get_height() - self.QUIT_BUTTON_SIZE / 2
            ),
            self.QUIT_BUTTON_SIZE
        )

        self.background_elements: [MenuElement] = []
        self.animated_elements: [MenuElement] = [self.quit_button]
        self.elements: [MenuElement] = [*self.animated_elements]
        self.run_display = True

    def add_animated_elements(self, *elements):
        self.animated_elements.extend(elements)
        self.add_elements(*elements)

    def add_elements(self, *elements):
        self.elements.extend(elements)

    def add_background_elements(self, *elements):
        """Saves elements that will be blit on the game surface (in the background)"""
        self.background_elements.extend(elements)

    def animate(self):
        for element in self.animated_elements:
            element.animate()

    def blit_elements(self):
        for element in self.background_elements:
            element.blit(self.game.surface)
        for element in self.elements:
            element.blit(self.menu_surface)

    def update_screen(self):
        self.menu_surface.fill(pygame.Color(0, 0, 0, 0))
        self.game.surface.blit(self.game.background, (0, 0))
        self.blit_elements()
        self.game.screen.blit(self.game.surface, (0, 0))
        self.game.screen.blit(self.menu_surface, self.menu_surface_position)
        self.blade.draw()
        pygame.display.update()

    def handle_input(self):
        if self.quit_button.checked:
            self.game.exit()

    def display(self):
        self.run_display = True
        while self.run_display:
            self.update()
            self.game.handle_events()
            self.handle_input()
            self.animate()
            self.update_screen()

    def switch_menu(self, target_menu: MenuInput):
        self.run_display = False
        self.game.display_menu(target_menu)

    def update(self):
        pass


class MainMenu(Menu):
    ORIGINAL_BUTTON_SIZE = window_config.WIDTH * .3
    MULTIPLAYER_BUTTON_SIZE = window_config.WIDTH * .25
    FRUIT_TEXT_IMAGE_WIDTH = window_config.WIDTH * .4
    NINJA_TEXT_IMAGE_WIDTH = window_config.WIDTH * .2
    NEW_TEXT_IMAGE_WIDTH = MULTIPLAYER_BUTTON_SIZE * .4

    def __init__(self, game):
        Menu.__init__(self, game)
        self.original_button = FruitButton(
            game,
            menu_config.ORIGINAL_INNER_IMAGE,
            menu_config.ORIGINAL_OUTER_IMAGE,
            Vector2(
                self.menu_surface.get_width() / 2,
                self.menu_surface.get_height() * .6
            ),
            self.ORIGINAL_BUTTON_SIZE
        )
        self.multiplayer_button = FruitButton(
            game,
            menu_config.MULTIPLAYER_INNER_IMAGE,
            menu_config.MULTIPLAYER_OUTER_IMAGE,
            Vector2(
                self.MULTIPLAYER_BUTTON_SIZE / 2,
                self.menu_surface.get_height() * .9 - self.MULTIPLAYER_BUTTON_SIZE / 2
            ),
            self.MULTIPLAYER_BUTTON_SIZE
        )
        self.backdrop_image = Image(
            menu_config.BACKDROP_IMAGE,
            Vector2(0, 0),
            window_config.WIDTH
        )
        self.fruit_text_image = Image(
            menu_config.FRUIT_TEXT_IMAGE,
            Vector2(menu_config.PADDING, menu_config.PADDING),
            self.FRUIT_TEXT_IMAGE_WIDTH
        )
        self.ninja_text_image = Image(
            menu_config.NINJA_TEXT_IMAGE,
            Vector2(
                2 * menu_config.PADDING + self.FRUIT_TEXT_IMAGE_WIDTH,
                menu_config.PADDING + self.fruit_text_image.height / 2
            ),
            self.NINJA_TEXT_IMAGE_WIDTH
        )
        self.new_text_image = Image(
            menu_config.NEW_TEXT_IMAGE,
            self.multiplayer_button.position + Vector2(self.multiplayer_button.width / 4, -self.multiplayer_button.height / 2),
            self.NEW_TEXT_IMAGE_WIDTH
        )

        self.add_animated_elements(self.original_button, self.multiplayer_button)
        self.add_background_elements(self.backdrop_image, self.fruit_text_image, self.ninja_text_image)
        self.add_elements(self.new_text_image)

    def handle_input(self):
        Menu.handle_input(self)
        match self.get_input():
            case MainMenuInput.ORIGINAL:
                self.switch_menu(MenuInput.ORIGINAL)
            case MainMenuInput.MULTIPLAYER:
                self.switch_menu(MenuInput.MULTIPLAYER)

    def get_input(self):
        if self.original_button.checked:
            return MainMenuInput.ORIGINAL
        if self.multiplayer_button.checked:
            return MainMenuInput.MULTIPLAYER
        return None


class OriginalModeMenu(Menu):
    CLASSIC_BUTTON_SIZE = window_config.WIDTH * .25
    ARCADE_BUTTON_SIZE = window_config.WIDTH * .25
    ZEN_BUTTON_SIZE = window_config.WIDTH * .25

    def __init__(self, game):
        Menu.__init__(self, game)
        self.classic_button = FruitButton(
            game,
            menu_config.CLASSIC_INNER_IMAGE,
            menu_config.CLASSIC_OUTER_IMAGE,
            Vector2(
                self.menu_surface.get_width() * .05 + self.CLASSIC_BUTTON_SIZE / 2,
                self.menu_surface.get_height() * .55
            ),
            self.CLASSIC_BUTTON_SIZE
        )
        self.arcade_button = FruitButton(
            game,
            menu_config.ARCADE_INNER_IMAGE,
            menu_config.ARCADE_OUTER_IMAGE,
            Vector2(
                self.menu_surface.get_width() / 2,
                self.menu_surface.get_height() * .95 - self.ARCADE_BUTTON_SIZE / 2
            ),
            self.ARCADE_BUTTON_SIZE
        )
        self.zen_button = FruitButton(
            game,
            menu_config.ZEN_INNER_IMAGE,
            menu_config.ZEN_OUTER_IMAGE,
            Vector2(
                self.menu_surface.get_width() * .95 - self.ZEN_BUTTON_SIZE / 2,
                self.menu_surface.get_height() * .55
            ),
            self.ZEN_BUTTON_SIZE
        )
        self.back_button = create_back_button(game, self.menu_surface)

        self.add_animated_elements(self.classic_button, self.arcade_button, self.zen_button)
        self.add_elements(self.back_button)

    def handle_input(self):
        Menu.handle_input(self)
        match self.get_input():
            case OriginalMenuInput.CLASSIC:
                ClassicMode(self.game).start_game()
            case OriginalMenuInput.ARCADE:
                ArcadeMode(self.game).start_game()
            case OriginalMenuInput.ZEN:
                ZenMode(self.game).start_game()
            case OriginalMenuInput.BACK:
                # Reset back button state to ensure that it won't be checked after reentering the gui
                self.back_button.reset()
                self.switch_menu(MenuInput.MAIN)

    def get_input(self):
        if self.classic_button.checked:
            return OriginalMenuInput.CLASSIC
        if self.arcade_button.checked:
            return OriginalMenuInput.ARCADE
        if self.zen_button.checked:
            return OriginalMenuInput.ZEN
        if self.back_button.checked:
            return OriginalMenuInput.BACK
        return None


class MultiplayerModeMenu(Menu):
    CLASSIC_ATTACK_BUTTON_SIZE = window_config.WIDTH * .25
    ZEN_DUEL_BUTTON_SIZE = window_config.WIDTH * .25
    BACK_BUTTON_SIZE = window_config.WIDTH * .2

    def __init__(self, game):
        Menu.__init__(self, game)
        self.classic_attack_button = FruitButton(
            game,
            menu_config.CLASSIC_ATTACK_INNER_IMAGE,
            menu_config.CLASSIC_ATTACK_OUTER_IMAGE,
            Vector2(
                self.menu_surface.get_width() / 2 - self.CLASSIC_ATTACK_BUTTON_SIZE * .75,
                self.menu_surface.get_height() / 2
            ),
            self.CLASSIC_ATTACK_BUTTON_SIZE
        )
        self.zen_duel_button = FruitButton(
            game,
            menu_config.ZEN_DUEL_INNER_IMAGE,
            menu_config.ZEN_DUEL_OUTER_IMAGE,
            Vector2(
                self.menu_surface.get_width() / 2 + self.ZEN_DUEL_BUTTON_SIZE * .75,
                self.menu_surface.get_height() / 2
            ),
            self.ZEN_DUEL_BUTTON_SIZE
        )
        self.back_button = create_back_button(game, self.menu_surface)

        self.add_animated_elements(self.classic_attack_button, self.zen_duel_button)
        self.add_elements(self.back_button)

    def handle_input(self):
        Menu.handle_input(self)
        match self.get_input():
            case MultiplayerMenuInput.CLASSIC_ATTACK:
                # ClassicAttack.start_game(self.game)
                print('comming soon')
            case MultiplayerMenuInput.ZEN_DUEL:
                # ClassicAttack.start_game(self.game)
                print('comming soon')
            case MultiplayerMenuInput.BACK:
                # Reset back button state to ensure that it won't be checked after reentering the gui
                self.back_button.reset()
                self.switch_menu(MenuInput.MAIN)

    def get_input(self):
        if self.classic_attack_button.checked:
            return MultiplayerMenuInput.CLASSIC_ATTACK
        if self.zen_duel_button.checked:
            return MultiplayerMenuInput.ZEN_DUEL
        if self.back_button.checked:
            return MultiplayerMenuInput.BACK
        return None


class GameOverMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.back_button = create_back_button(game, self.menu_surface)
        self.game_over_text = self.font.render('Game over', True, 'White')
        self.game_over_label = ScoreLabel(
            self.game_over_text,
            Vector2(
                self.menu_surface.get_width() // 2 - self.game_over_text.get_width() // 2,
                self.menu_surface.get_height() // 2 - self.game_over_text.get_height() // 2
            )
        )

        self.add_elements(self.back_button, self.game_over_label)

    def handle_input(self):
        Menu.handle_input(self)
        match self.get_input():
            case GameOverMenuInputEnum.BACK:
                self.back_button.reset()
                self.switch_menu(MenuInput.MAIN)

    def get_input(self):
        if self.back_button.checked:
            return GameOverMenuInputEnum.BACK
        return None
2

class SinglePlayerGameOverMenu(GameOverMenu):
    def __init__(self, game, score):
        GameOverMenu.__init__(self, game)
        self.score_text = self.font.render(f'Your Score: {score}', True, 'White')
        self.score_label = ScoreLabel(
            self.score_text,
            Vector2(
                self.menu_surface.get_width() // 2 - self.score_text.get_width() // 2,
                self.menu_surface.get_height() // 2 - self.score_text.get_height() // 2 + self.game_over_text.get_width() // 2
            )
        )
        self.add_elements(self.score_label)


class MultiPlayerGameOverMenu(GameOverMenu):
    def __init__(self, game):
        GameOverMenu.__init__(self, game)
