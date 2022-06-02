import pygame
from pygame.math import Vector2
from .common import SinglePlayerMode
from src.app.items.items_spawner import ClassicModeItemSpawner
from src.app.controllers.gravity_controller import GravityController
from src.app.gui.bars import HealthBar
from src.config import classic_mode_config, window_config


class ClassicMode(SinglePlayerMode):
    def __init__(self, game):
        SinglePlayerMode.__init__(self, game)

        self.background = pygame.transform.scale(
            pygame.image.load(classic_mode_config.BACKGROUND_PATH),
            (window_config.WIDTH, window_config.HEIGHT)
        )

        self.gravity_controller = GravityController(Vector2(0, 600))
        self.item_spawner = ClassicModeItemSpawner(self.fruits, self.bombs)
        self.health_bar = HealthBar(classic_mode_config.LIVES)

        # Current state
        self.lives = classic_mode_config.LIVES

    def start_game(self):
        self.time_controller.start()
        self.game.start_game(self)

    def handle_fruit_collision(self, fruit):
        SinglePlayerMode.handle_fruit_collision(self, fruit)
        self.score_controller.register_fruit_cut()

    def handle_bomb_collision(self, bomb):
        SinglePlayerMode.handle_bomb_collision(self, bomb)
        self.decrease_lives()

    def decrease_lives(self):
        self.lives -= 1
        self.health_bar.update_lives(self.lives)
        if self.lives == 0:
            self.game.game_over()

    def update(self):
        SinglePlayerMode.update(self)
        self.update_difficulty()
        self.item_spawner.update()
        self.health_bar.blit(self.game.surface)

    def handle_out_of_bounds(self):
        self.decrease_lives()

    def update_difficulty(self):
        # updating interval and intensity based on time elapsed since beginning of the game
        self.item_spawner.set_interval(
            max(1.5, min(2, - self.time_controller.total_elapsed_time // 15))
        )
        self.item_spawner.set_intensity(
            max(3 , min(6, 1 + self.time_controller.total_elapsed_time // 8))
        )
