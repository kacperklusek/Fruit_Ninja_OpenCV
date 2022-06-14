import pygame
from src.app.gui.bars import ScoreBar, TimeBar
from .singleplayer_mode import SinglePlayerMode
from src.config import zen_mode_config, window_config
from src.app.items.item_spawner import ZenModeItemSpawner
from src.app.controllers.gravity_controller import GravityController


class ZenMode(SinglePlayerMode):
    def __init__(self, game):
        SinglePlayerMode.__init__(self, game)

        self.background = pygame.transform.scale(
            pygame.image.load(zen_mode_config.BACKGROUND_PATH),
            (window_config.WIDTH, window_config.HEIGHT)
        )

        self.gravity_controller = GravityController(pygame.Vector2(0, 600))
        self.item_spawner = ZenModeItemSpawner(self._fruits, self._bombs, self.notify_item_spawn)

        self.score_bar = ScoreBar(self.score_controller)
        self.time_bar = TimeBar(zen_mode_config.TIME)
        self.hud_elements.extend([self.score_bar, self.time_bar])

    def start_game(self):
        self.time_controller.start()

    def update(self):
        SinglePlayerMode.update(self)
        self.score_controller.check_combo_finished()
        self.update_difficulty()
        self.item_spawner.update()
        self.time_bar.update_time(self.time_controller.total_elapsed_time)
        self.check_time()

    def check_time(self):
        if self.time_controller.total_elapsed_time >= zen_mode_config.TIME:
            self.game_over()

    def update_difficulty(self):
        gameplay_time = self.time_controller.total_elapsed_time
        self.item_spawner.intensity = int(gameplay_time // 10) + 2
        self.item_spawner.interval = .3 + max((2000 - gameplay_time) / 2000, 0)

    def handle_out_of_bounds(self):
        pass
