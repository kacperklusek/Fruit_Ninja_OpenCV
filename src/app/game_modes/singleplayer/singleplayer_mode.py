from src.app.controllers.score_controller import ScoreController
from src.app.game_modes.game_mode import GameModeCommon
from pygame.sprite import Group
from abc import ABC


class SinglePlayerMode(GameModeCommon, ABC):
    def __init__(self, game):
        GameModeCommon.__init__(self, game)
        self.score_controller = ScoreController(self.labels)
        self.items_surface = self._create_surface()

        # Current state
        self._fruits = Group()
        self._bombs = Group()

    @property
    def blade(self):
        return self.game.blade

    @property
    def score(self):
        return self.score_controller.score

    def handle_collisions(self):
        for bomb in self._bombs:
            if self.blade.collides(bomb):
                self.handle_bomb_collision(bomb)
        for fruit in self._fruits:
            if self.blade.collides(fruit):
                self.handle_fruit_collision(fruit)

    def handle_fruit_collision(self, fruit):
        GameModeCommon.handle_fruit_collision(self, fruit)
        self.score_controller.register_fruit_cut(fruit)

    def handle_bomb_collision(self, bomb):
        self.game.notify_bomb_collision()
        self.kill_fruits()
        bomb.kill()

    def kill_fruits(self):
        for fruit in self._fruits:
            fruit.kill()

    def blit_items(self):
        self._fruits.update(out_of_bounds_handler=self.handle_out_of_bounds)
        self._bombs.update()
        self._fruits.draw(self.items_surface)
        self._bombs.draw(self.items_surface)

    def update(self):
        GameModeCommon.update(self)
        self.items_surface.fill(self.EMPTY_COLOR)
        self.handle_collisions()
        self.blit_items()
        self.game.screen.blit(self.items_surface, (0, 0))

    def clear(self):
        GameModeCommon.clear(self)
        for fruit in self._fruits:
            fruit.kill()
        for bomb in self._bombs:
            bomb.kill()

    def game_over(self):
        self.game.game_over()
