import pygame

from src.app.effects.blade import Blade
from src.app.items.bombs.bomb import Bomb
from src.app.items.fruits.fruit import Fruit
from src.app.items.item import Item
from src.app.items.items_spawner import ItemsSpawner
from src.app.physics.time_controller import TimeController


class Game:
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
        self.fruit_spawner = ItemsSpawner(config.fruit,
                                          config.bomb,
                                          self.time_controller,
                                          self.config.DIFFICULTY)

        # Game state
        self.game_active = True
        self.score = 0
        self.lives = self.config.LIFES
        self.stats = None

    def start(self):
        while True:
            self.time_controller.update_last_frame_time()
            self.handle_events()
            self.update()
            self.clock.tick(self.config.FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.blade.input_source.end_tracking()
                pygame.quit()
                exit()

    def update(self):
        self.surface.blit(self.background, (0, 0))

        # TODO - extract this method to handle_collisions
        # check collision and remove colliding
        if self.blade:
            for fruit in Fruit.group:
                if fruit.rect.collidepoint(self.blade[-1]):
                    fruit.kill()
                    self.score += 1
            for bomb in Bomb.group:
                if bomb.rect.collidepoint(self.blade[-1]):
                    self.handle_bomb_collision(bomb)

        if self.lives <= Item.out_of_bounds:
            self.game_active = False

        self.update_items()
        self.blade.draw()
        self.fruit_spawner.update()
        pygame.display.update()

    def update_difficulty(self):
        ...
        # self.fruit_spawner.

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

    def handle_bomb_collision(self, bomb):
        for fruit in Fruit.group:
            fruit.kill()
        bomb.kill()
        self.lives -= 1
        if self.lives <= Item.out_of_bounds:
            print("GAME OVER")
            self.game_active = False
