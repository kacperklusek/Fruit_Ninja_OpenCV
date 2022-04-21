import pygame

from src.app.effects.blade import Blade
from src.app.items.bombs.bomb import Bomb
from src.app.items.fruits.fruit import Fruit
from src.app.items.items_spawner import ItemsSpawner


class Game:
    def __init__(self, config):
        # Data
        self.config = config.game

        # Pygame
        self.screen = pygame.display.set_mode((self.config.WIDTH, self.config.HEIGHT))
        self.clock = pygame.time.Clock()
        self.surface = pygame.Surface((self.config.WIDTH, self.config.HEIGHT))
        pygame.display.set_caption(self.config.TITLE)

        # Sprites
        self.blade = Blade(config.blade, self.screen)

        # Fruits
        self.fruit_spawner = ItemsSpawner(self.config.FRUIT_FREQUENCY, self.config.BOMB_FREQUENCY)

        # Game state
        self.game_active = True

        # Initialize the game
        self.init()

    def init(self):
        pygame.init()

    def start(self):
        while True:
            self.surface.fill(self.config.BACKGROUND_COLOR)
            self.handle_events()

            # TODO - extract this method to handle_collisions
            # check collision and remove colliding
            if self.blade:
                for fruit in Fruit.group:
                    if fruit.rect.collidepoint(self.blade.get_last_point()):
                        fruit.kill()

            self.fruit_spawner.handle_spawning()
            self.update_items()
            self.blade.draw()
            pygame.display.update()
            self.clock.tick(self.config.FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.blade.input_source.end_tracking()
                pygame.quit()
                exit()

    def update_items(self):
        self.update_fruits()
        self.update_bombs()
        self.screen.blit(self.surface, (0, 0))

    def update_bombs(self):
        Bomb.group.update()
        Bomb.group.draw(self.surface)

    def update_fruits(self):
        Fruit.group.update()
        Fruit.group.draw(self.surface)
