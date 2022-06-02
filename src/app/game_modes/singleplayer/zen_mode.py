import pygame

from src.config import zen_mode_config, window_config
from .singleplayer_mode import SinglePlayerMode
from ...controllers.gravity_controller import GravityController
from ...gui.bars import ScoreBar
from ...items.item_spawner import ZenModeItemSpawner


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
        self.hud_elements.extend([self.score_bar])

    def start_game(self):
        self.time_controller.start()

    def handle_fruit_collision(self, fruit):
        SinglePlayerMode.handle_fruit_collision(self, fruit)
        self.score_controller.register_fruit_cut(fruit)

    def handle_bomb_collision(self, bomb):
        SinglePlayerMode.handle_bomb_collision(self, bomb)
        self.game_over()

    def update(self):
        SinglePlayerMode.update(self)
        self.score_controller.check_combo_finished()
        self.update_difficulty()
        self.item_spawner.update()

    def update_difficulty(self):
        gameplay_time = self.time_controller.total_elapsed_time
        self.item_spawner.intensity = int(gameplay_time // 20) + 2
        self.item_spawner.interval = .5 + max((1000 - gameplay_time) / 500, 0)
        self.item_spawner.bomb_probability = min(.15 + gameplay_time / 2000, .3)

    def handle_out_of_bounds(self):
        pass
