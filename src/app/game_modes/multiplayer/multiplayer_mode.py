from abc import ABC
from pygame.font import Font
from pygame.math import Vector2
from src.app.gui.menus import MenuInput
from src.app.utils.timeouts import Timeout
from src.app.gui.labels import AnimatedLabel
from src.app.game_modes.game_mode import GameModeCommon
from src.config import multi_player_mode_config, window_config, game_config


# TODO - TO BE IMPLEMENTED
class MultiPlayerMode(GameModeCommon, ABC):
    def __init__(self, game):
        GameModeCommon.__init__(self, game)

        font = Font(game_config.FONT, game_config.FONT_SIZE)
        self.coming_soon_label = AnimatedLabel(
            [font.render('Coming soon', True, game_config.DEFAULT_FONT_COLOR)],
            Vector2(window_config.WIDTH / 2, window_config.HEIGHT / 2),
            multi_player_mode_config.COMING_SOON_DISPLAY_DURATION,
            self.labels
        )

        Timeout(
            self.redirect_to_main_menu,
            multi_player_mode_config.COMING_SOON_DISPLAY_DURATION
        )

    def redirect_to_main_menu(self):
        self.game.game_active = False
        self.game.display_menu(MenuInput.MAIN)

    def start_game(self):
        pass
