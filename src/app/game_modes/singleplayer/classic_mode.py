import pygame
from pygame.math import Vector2
from .singleplayer_mode import SinglePlayerMode
from src.app.items.item_spawner import ClassicModeItemSpawner
from src.app.controllers.gravity_controller import GravityController
from src.app.gui.bars import HealthBar, ScoreBar
from src.config import classic_mode_config, window_config


class ClassicMode(SinglePlayerMode):
    def __init__(self, game):
        SinglePlayerMode.__init__(self, game)

        self.background = pygame.transform.scale(
            pygame.image.load(classic_mode_config.BACKGROUND_PATH),
            (window_config.WIDTH, window_config.HEIGHT)
        )

        self.gravity_controller = GravityController(Vector2(0, 600))
        self.item_spawner = ClassicModeItemSpawner(self._fruits, self._bombs, self.notify_item_spawn)

        self.health_bar = HealthBar(classic_mode_config.LIVES)
        self.score_bar = ScoreBar(self.score_controller)
        self.hud_elements.extend([self.health_bar, self.score_bar])

        # Current state
        self.lives = classic_mode_config.LIVES

    def start_game(self):
        self.time_controller.start()

    def handle_fruit_collision(self, fruit):
        SinglePlayerMode.handle_fruit_collision(self, fruit)
        self.score_controller.register_fruit_cut(fruit)

    def handle_bomb_collision(self, bomb):
        SinglePlayerMode.handle_bomb_collision(self, bomb)
        self.game_over()

    def decrease_lives(self):
        self.lives -= 1
        self.health_bar.update_lives(self.lives)
        if self.lives == 0:
            self.game_over()

    def update(self):
        SinglePlayerMode.update(self)
        self.score_controller.check_combo_finished(self.effects_surface)
        self.update_difficulty()
        self.item_spawner.update()

    def handle_out_of_bounds(self):
        self.decrease_lives()

    def update_difficulty(self):
        gameplay_time = self.time_controller.total_elapsed_time
        self.item_spawner.intensity = int(gameplay_time // 20) + 2
        self.item_spawner.interval = .5 + max((1000 - gameplay_time) / 500, 0)
        self.item_spawner.bomb_probability = min(.15 + gameplay_time / 2000, .3)
