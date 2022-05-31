import pygame
from time import time
from random import randint

from pygame.math import Vector2
from src.app.control.blade import Blade
from src.app.items.bomb import Bomb
from src.app.items.fruit import Fruit
from src.app.items.item import Item
from src.app.items.items_spawner import ItemsSpawner
from src.app.physics.time_controller import TimeController
from src.app.items.fruit import PlainFruit, GravityFruit, FreezeFruit
from src.app.physics.gravity_controller import GravityController
from src.app.utils.enums.input_source import InputSource
from src.app.effects.sounds import SoundController
from src.app.menu.menu import MainMenu


from src.config import window_config, game_modes_config, game_config


class Game:
    COMBO_TIME_DIFF = 0.2
    COMBO_FACTOR = 2
    SCREEN_SHAKE_DURATION = 55
    SCREEN_SHAKE_OFFSET = 100

    def __init__(self):
        # Pygame
        pygame.init()
        self.background = pygame.transform.scale(
            pygame.image.load(window_config.BACKGROUND_PATH), (window_config.WIDTH, window_config.HEIGHT)
        )
        self.screen = pygame.display.set_mode((window_config.WIDTH, window_config.HEIGHT))
        self.clock = pygame.time.Clock()
        self.surface = pygame.Surface((window_config.WIDTH, window_config.HEIGHT))
        self.font = pygame.font.Font("freesansbold.ttf", 25)
        pygame.display.set_caption(window_config.TITLE)

        # Sprites
        self.blade = Blade(self.screen, game_config.INPUT_SOURCE)

        # Utilities
        self.time_controller = TimeController()
        self.gravity_controller = GravityController()
        self.item_spawner = ItemsSpawner(game_modes_config.CLASSIC.DIFFICULTY)  # TODO - implement more game modes
        self.gravity_controller.gravity = Vector2(0, 600)

        # Game state
        self.game_active = True
        self.score = 0

        self.lives = game_modes_config.CLASSIC.LIVES
        self.combo = 0
        self.stats = None

        self.last_fruit_kill_time = 0
        self.prev_ratio = self.time_controller.ratio

        self.freeze_start_time = 0
        self.gravity_start_time = 0
        self.gravity_bonus_enabled = False
        self.freeze_bonus_enabled = False
        self.game_started = False

        # Screen Shaking
        self.screen_shake = 0

        # Menu
        self.menu = MainMenu(self)

    def start(self):
        self.time_controller.init()
        self.game_active = True
        self.score = 0
        self.lives = game_modes_config.CLASSIC.LIVES
        self.stats = None

        SoundController.play_game_start_sound()

        while True:
            self.handle_events()
            self.time_controller.register_new_frame()
            self.update()
            self.update_difficulty()
            self.clock.tick(game_config.FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.blade.input_source.end_tracking()
                pygame.quit()
                exit()

    def update(self):
        render_offset = [0, 0]
        if self.screen_shake:
            self.screen_shake -= 1
            render_offset = [randint(0, self.SCREEN_SHAKE_OFFSET) - self.SCREEN_SHAKE_OFFSET//2,
                             randint(0, self.SCREEN_SHAKE_OFFSET) - self.SCREEN_SHAKE_OFFSET//2]

        self.surface.blit(self.background, render_offset)
        self.screen.blit(self.surface, (0, 0))

        if self.game_started:
            self.update_items()
            if self.game_active:
                if Item.out_of_bounds >= self.lives:
                    self.game_active = False
                    SoundController.play_game_over_sound()

                self.handle_collisions()
                self.check_combo_finish()
                self.update_bonus()
                self.item_spawner.update()
            else:
                text = self.font.render('Game over', True, 'White')
                self.screen.blit(text, (window_config.WIDTH // 2, window_config.HEIGHT // 2))
        else:
            self.menu.display()


        self.blade.draw()
        pygame.display.update()

    def update_difficulty(self):
        self.item_spawner.intensity = min(1 + self.time_controller.total_elapsed_time // 8, 5)
        self.item_spawner.interval = max(2.5 - self.time_controller.total_elapsed_time / 15, 1.5)

    def update_items(self):
        self.update_fruits()
        self.update_bombs()
        self.update_score_and_hp()
        self.screen.blit(self.surface, (0, 0))

    def update_score_and_hp(self):
        self.stats = self.font.render(f'score: {self.score}  \
        <3: {max(0, self.lives - Item.out_of_bounds)}',
                                      True,
                                      'White')
        self.surface.blit(self.stats, self.stats.get_rect())

    def update_bombs(self):
        Bomb.group.update(self.time_controller.last_frame_duration)
        Bomb.group.draw(self.surface)

    def update_fruits(self):
        Fruit.group.update(self.time_controller.last_frame_duration)
        Fruit.group.draw(self.surface)

    def handle_collisions(self):
        if self.blade:
            for fruit in Fruit.group:
                if self.blade.collides(fruit):
                    fruit.kill()
                    self.handle_score_update()
                    if not isinstance(fruit, PlainFruit):
                        self.start_bonus(fruit)
                    SoundController.play_splatter_sound()

            for bomb in Bomb.group:
                if self.blade.collides(bomb):
                    self.handle_bomb_collision(bomb)
                    SoundController.play_boom_sound()
                    self.screen_shake = self.SCREEN_SHAKE_DURATION

    def handle_score_update(self):
        curr_time = time()
        if curr_time - self.last_fruit_kill_time <= self.COMBO_TIME_DIFF:
            if self.combo == 0:
                self.score -= 1
                self.combo += 1
            self.combo += 1
        else:
            self.score += 1
        self.last_fruit_kill_time = curr_time

    # checks if combo has finished
    def check_combo_finish(self):
        if self.combo > 0 and time() - self.last_fruit_kill_time > self.COMBO_TIME_DIFF:
            self.score += self.combo * self.COMBO_FACTOR
            # TODO display combo info on the screen for certain amount of time
            print(f"COMBOOOOO {self.combo} !!!!!")
            self.combo = 0

    def handle_bomb_collision(self, bomb):
        for fruit in Fruit.group:
            fruit.kill()
        bomb.kill()
        self.lives -= 1

    def start_bonus(self, fruit):
        if isinstance(fruit, GravityFruit):
            self.gravity_bonus_enabled = True
            self.gravity_start_time = time()
            self.gravity_controller.gravity = Vector2(0, -600)
        elif isinstance(fruit, FreezeFruit):
            self.freeze_bonus_enabled = True
            self.freeze_start_time = time()
            self.time_controller.ratio = .4

    def update_bonus(self):
        curr_time = time()

        if self.gravity_bonus_enabled and curr_time - self.gravity_start_time > 10:
            self.gravity_bonus_enabled = False
            self.freeze_start_time = time()
            self.gravity_controller.gravity = Vector2(0, 600)

        if self.freeze_bonus_enabled and curr_time - self.freeze_start_time > 10:
            self.time_controller.ratio = self.prev_ratio
            self.freeze_bonus_enabled = False
