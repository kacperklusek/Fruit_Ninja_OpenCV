import time
import pygame
from pygame.font import Font
from pygame.math import Vector2
from .singleplayer_mode import SinglePlayerMode

from src.app.gui.labels import AnimatedLabel
from src.app.gui.bars import ScoreBar, TimeBar
from src.app.utils.enums import ItemType, BonusType
from src.app.items.item_spawner import ArcadeModeItemSpawner
from src.app.controllers.gravity_controller import GravityController
from src.config import window_config, arcade_mode_config, game_config


class ArcadeMode(SinglePlayerMode):
    def __init__(self, game):
        SinglePlayerMode.__init__(self, game)

        self.background = pygame.transform.scale(
            pygame.image.load(arcade_mode_config.BACKGROUND_PATH),
            (window_config.WIDTH, window_config.HEIGHT)
        )

        self.gravity_controller = GravityController(Vector2(0, 600))
        self.item_spawner = ArcadeModeItemSpawner(self._fruits, self._bombs, self.notify_item_spawn)

        self.score_bar = ScoreBar(self.score_controller)
        self.time_bar = TimeBar(arcade_mode_config.TIME)
        self.hud_elements.extend([self.score_bar, self.time_bar])

        self.gravity_bonus_enabled = False
        self.gravity_start_time = 0

        self.freeze_bonus_enabled = False
        self.freeze_bonus_start_time = 0

    def start_game(self):
        self.time_controller.start()

    def handle_gravity_change(self):
        if not self.gravity_bonus_enabled:
            self.gravity_bonus_enabled = True
            self.gravity_controller.gravity *= -1
        self.gravity_start_time = time.time()

    def handle_freeze(self):
        if not self.freeze_bonus_enabled:
            self.freeze_bonus_enabled = True
            self.time_controller.ratio = arcade_mode_config.FREEZE_RATIO
        self.freeze_bonus_start_time = time.time()

    def handle_fruit_collision(self, fruit):
        SinglePlayerMode.handle_fruit_collision(self, fruit)

        if fruit.TYPE == ItemType.BONUS_FRUIT:
            match fruit.BONUS_TYPE:
                case BonusType.FREEZE:
                    self.handle_freeze()
                case BonusType.GRAVITY:
                    self.handle_gravity_change()

    def handle_bomb_collision(self, bomb):
        SinglePlayerMode.handle_bomb_collision(self, bomb)
        points_decrease = arcade_mode_config.BOMB_COLLISION_POINTS_DECREASE
        self.score_controller.score -= points_decrease

        AnimatedLabel([
            Font(game_config.FONT, 50).render(f'-{points_decrease}', True, arcade_mode_config.DECREASE_POINTS_COLOR),
        ],
            bomb.position,
            arcade_mode_config.DECREASE_POINTS_VISIBILITY_DURATION,
            self.labels
        )

    def update_bonuses(self):
        curr_time = time.time()
        if self.gravity_bonus_enabled and \
                curr_time - self.gravity_start_time > arcade_mode_config.GRAVITY_CHANGE_DURATION:
            self.gravity_bonus_enabled = False
            self.gravity_controller.gravity *= -1

        if self.freeze_bonus_enabled and \
                curr_time - self.freeze_bonus_start_time > arcade_mode_config.FREEZE_DURATION:
            self.freeze_bonus_enabled = False
            self.time_controller.ratio = 1

    def update(self):
        SinglePlayerMode.update(self)
        self.score_controller.check_combo_finished()
        self.update_difficulty()
        self.item_spawner.update()
        self.time_bar.update_time(self.time_controller.total_elapsed_time)
        self.check_time()
        self.update_bonuses()

    def check_time(self):
        if self.time_controller.total_elapsed_time >= arcade_mode_config.TIME:
            self.game_over()

    def update_difficulty(self):
        gameplay_time = self.time_controller.total_elapsed_time
        self.item_spawner.intensity = int(gameplay_time // 15) + 5
        self.item_spawner.interval = .25 + max((1000 - gameplay_time) / 500, 0)
        self.item_spawner.bomb_probability = min(.15 + gameplay_time / 2000, .3)
        self.item_spawner.bonus_item_probability = min(.05 + gameplay_time / 4000, .1)

    def handle_out_of_bounds(self):
        pass
