import pygame

from src.app.effects.blade import Blade
from src.app.items.bombs.bomb import Bomb
from src.app.items.fruits.fruit import Fruit
from src.app.items.item import Item
from src.app.items.items_spawner import ItemsSpawner


class Game:
    font = None
    lives = None    # TODO - change this to the instance attribute

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
        self.fruit_spawner = ItemsSpawner(config.fruit, config.bomb)

        # Game state
        self.game_active = True
        self.score = 0
        self.lives = self.config.LIFES
        self.stats = None

        # Initialize the game
        self.init()

    def init(self):
        pygame.init()
        self.font = pygame.font.Font("freesansbold.ttf", 25)

    def start(self):
        while True:
            self.surface.fill(self.config.BACKGROUND_COLOR)
            self.handle_events()

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

            if self.game_active:
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

    def handle_bomb_collision(self, bomb):
        for fruit in Fruit.group:
            fruit.kill()
        bomb.kill()
        self.lives -= 1
        if self.lives <= Item.out_of_bounds:
            print("GAME OVER")
            self.game_active = False

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
        Bomb.group.update()
        Bomb.group.draw(self.surface)

    def update_fruits(self):
        Fruit.group.update()
        Fruit.group.draw(self.surface)
