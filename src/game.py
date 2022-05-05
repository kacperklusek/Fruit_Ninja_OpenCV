import pygame
from time import time

from src.app.effects.blade import Blade
from src.app.items.bombs.bomb import Bomb
from src.app.items.fruits.fruit import Fruit
from src.app.items.item import Item
from src.app.items.items_spawner import ItemsSpawner
from src.app.physics.time_controller import TimeController


class Game:
    # TODO move this to config, i would but mateusz is making changes to config files
    COMBO_TIME_DIFF = 0.2
    COMBO_FACTOR = 2

    def __init__(self, config):
        # Data
        self.config = config.game

        # Pygame
        pygame.init()
        self.background = pygame.transform.scale(
            pygame.image.load(self.config.BACKGROUND_PATH), (self.config.WIDTH, self.config.HEIGHT)
        )
        self.screen = pygame.display.set_mode((self.config.WIDTH, self.config.HEIGHT))
        self.clock = pygame.time.Clock()
        self.surface = pygame.Surface((self.config.WIDTH, self.config.HEIGHT))
        self.font = pygame.font.Font("freesansbold.ttf", 25)
        pygame.display.set_caption(self.config.TITLE)

        # Sprites
        self.blade = Blade(config.blade, self.screen)

        # Utilities
        self.time_controller = TimeController()
        self.item_spawner = ItemsSpawner(
            config.fruits,
            config.bomb,
            self.time_controller,
            self.config.DIFFICULTY
        )

        # Game state
        self.game_active = True
        self.score = 0
        self.combo = 0
        self.lives = self.config.LIVES
        self.stats = None

    def start(self):
        self.time_controller.init_game_timing()
        self.game_active = True
        self.score = 0
        self.lives = self.config.LIVES
        self.stats = None

        while self.game_active:
            self.time_controller.update_last_frame_time()
            self.handle_events()
            self.update()
            self.update_difficulty()
            self.clock.tick(self.config.FPS)

        #TODO - add new game

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.blade.input_source.end_tracking()
                pygame.quit()
                exit()

    def update(self):
        self.surface.blit(self.background, (0, 0))

        self.handle_collisions()
        self.check_combo_finish()

        if Item.out_of_bounds >= self.lives:
            self.game_active = False

        self.update_items()
        self.blade.draw()
        self.item_spawner.update()
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
        Bomb.group.update(self.time_controller.get_last_frame_duration)
        Bomb.group.draw(self.surface)

    def update_fruits(self):
        Fruit.group.update(TimeController.get_last_frame_duration)
        Fruit.group.draw(self.surface)

    def handle_collisions(self):
        if self.blade:
            for fruit in Fruit.group:
                if fruit.rect.collidepoint(self.blade[-1]):
                    fruit.kill()
                    self.handle_score_update()
            for bomb in Bomb.group:
                if bomb.rect.collidepoint(self.blade[-1]):
                    self.handle_bomb_collision(bomb)

    def handle_score_update(self):
        if time() - TimeController.last_fruit_kill_time <= self.COMBO_TIME_DIFF:
            if self.combo == 0:
                self.score -= 1
                self.combo += 1
            self.combo += 1
        else:
            self.score += 1
        TimeController.update_last_fruit_kill()

    # checks if combo has finished
    def check_combo_finish(self):
        if self.combo > 0 and time() - TimeController.last_fruit_kill_time > self.COMBO_TIME_DIFF:
            self.score += self.combo * self.COMBO_FACTOR
            # TODO display combo info on the screen for certain amount of time
            print(f"COMBOOOOO {self.combo} !!!!!")
            self.combo = 0


    def handle_bomb_collision(self, bomb):
        for fruit in Fruit.group:
            fruit.kill()
        bomb.kill()
        self.lives -= 1
        if self.lives <= Item.out_of_bounds:
            print("GAME OVER")
            self.game_active = False
