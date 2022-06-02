from pygame.font import Font
from random import randint
import pygame
import sys

from src.app.control.blade import Blade
from src.app.utils.enums import GameMode
from src.app.items.fruit import SlicedFruit
from src.app.effects.sounds import SoundController
from src.app.controllers.time_controller import TimeController
from src.app.game_modes.singleplayer.classic_mode import ClassicMode
from src.app.gui.menus import MainMenu, OriginalModeMenu, MultiplayerModeMenu, GameOverMenu, MenuInput, \
    SinglePlayerGameOverMenu

from src.config import window_config, game_config


class Game:
    SCREEN_SHAKE_DURATION = 100
    SCREEN_SHAKE_OFFSET = 70

    def __init__(self):
        # Pygame
        self.init()
        self.clock = pygame.time.Clock()
        self.font = Font(game_config.FONT, game_config.FONT_SIZE)

        self.screen = pygame.display.set_mode((window_config.WIDTH, window_config.HEIGHT), pygame.RESIZABLE)
        self.surface = pygame.Surface((window_config.WIDTH, window_config.HEIGHT), pygame.SRCALPHA)
        self.background = pygame.transform.scale(
            pygame.image.load(window_config.BACKGROUND_PATH),
            (window_config.WIDTH, window_config.HEIGHT)
        )

        # Controllers
        self.time_controller = TimeController()

        # Input
        self.blade = Blade(self.screen, game_config.INPUT_SOURCE)

        # Game state
        self.game_active = True  # TODO
        self.game_mode = None

        # Menus
        self.main_menu = MainMenu(self)
        self.original_menu = OriginalModeMenu(self)
        self.multiplayer_menu = MultiplayerModeMenu(self)
        self.game_over_menu = GameOverMenu(self)
        self.curr_menu = self.original_menu

        # Screen Shaking
        self.render_offset = [0, 0]
        self.remaining_screen_shake_duration = 0

    @staticmethod
    def init():
        pygame.init()
        pygame.mouse.set_visible(False)
        pygame.display.set_icon(pygame.image.load(window_config.ICON_PATH))
        pygame.display.set_caption(window_config.TITLE)

    def start(self):
        SoundController.play_menu_sound()
        self.curr_menu.display()

    def reset(self):
        self.game_active = True
        self.remaining_screen_shake_duration = 0

    def exit(self):
        self.blade.destroy()
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()

    def display_menu(self, menu: MenuInput):
        match menu:
            case MenuInput.MAIN:
                self.curr_menu = self.main_menu
            case MenuInput.ORIGINAL:
                self.curr_menu = self.original_menu
            case MenuInput.MULTIPLAYER:
                self.curr_menu = self.multiplayer_menu
            case MenuInput.SINGLE_PLAYER_GAME_OVER_MENU:
                self.curr_menu = SinglePlayerGameOverMenu(self, self.game_mode.score)
            case _:
                return

        self.curr_menu.display()

    def start_game(self, game_mode):    # TODO add parent class for single and multiplayer gamemode
        self.reset()
        self.game_mode = game_mode

        SoundController.stop_menu_sound()
        SoundController.play_game_start_sound()

        while self.game_active:
            self.game_update()

    def game_over(self):
        SoundController.play_game_over_sound()
        self.game_active = False
        self.display_menu(MenuInput.SINGLE_PLAYER_GAME_OVER_MENU) # TODO match game mode

    def game_update(self):
        self.time_controller.register_new_frame()
        self.handle_events()

        self.render_offset = (0, 0)
        if self.remaining_screen_shake_duration:
            self.apply_screen_shake()

        self.surface.blit(self.background, self.render_offset)
        self.blit_sliced_fruits()
        self.game_mode.update()
        self.screen.blit(self.surface, (0, 0))
        self.blade.draw()

        self.clock.tick(game_config.FPS)
        pygame.display.update()

    def blit_sliced_fruits(self):
        SlicedFruit.group.update(self.time_controller.last_frame_duration)
        SlicedFruit.group.draw(self.surface)

    def notify_bomb_collision(self):
        self.remaining_screen_shake_duration = self.SCREEN_SHAKE_DURATION
        SoundController.play_boom_sound()

    def apply_screen_shake(self):
        self.remaining_screen_shake_duration -= 1
        self.render_offset = (
            randint(0, self.SCREEN_SHAKE_OFFSET) - self.SCREEN_SHAKE_OFFSET // 2,
            randint(0, self.SCREEN_SHAKE_OFFSET) - self.SCREEN_SHAKE_OFFSET // 2
        )
