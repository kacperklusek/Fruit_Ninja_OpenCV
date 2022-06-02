from pygame.sprite import Group
from src.app.controllers.score_controller import ScoreController
from src.app.controllers.time_controller import TimeController
from abc import ABC, abstractmethod


class SinglePlayerMode(ABC):
    def __init__(self, game):
        self.game = game
        self.time_controller = TimeController()
        self.score_controller = ScoreController()

        # Current state
        self.fruits = Group()
        self.bombs = Group()

    @abstractmethod
    def start_game(self):
        pass

    @property
    def blade(self):
        return self.game.blade

    @property
    def score(self):
        return self.score_controller.score

    def handle_collisions(self):
        for bomb in self.bombs:
            if self.blade.collides(bomb):
                self.handle_bomb_collision(bomb)
        for fruit in self.fruits:
            if self.blade.collides(fruit):
                self.handle_fruit_collision(fruit)

    def handle_bomb_collision(self, bomb):
        self.game.notify_bomb_collision()
        self.kill_fruits()
        bomb.kill()

    def handle_fruit_collision(self, fruit):
        fruit.kill()

    def kill_fruits(self):
        for fruit in self.fruits:
            fruit.kill()  # TODO - add splash effect

    def blit(self):
        duration = self.time_controller.last_frame_duration
        self.fruits.update(duration, self.handle_out_of_bounds)
        self.bombs.update(duration)
        self.fruits.draw(self.game.surface)
        self.bombs.draw(self.game.surface)

    @abstractmethod
    def handle_out_of_bounds(self):
        pass

    def update(self):
        self.handle_collisions()
        self.score_controller.check_combo_finished()
        self.blit()
