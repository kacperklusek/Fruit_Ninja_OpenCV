import time

from pygame.math import Vector2

from random import randint

from src.app.items.bombs.bomb import Bomb
from src.app.items.fruits.fruit import Fruit
from src.app.items.fruits.fruit_type import FruitType
from src.app.physics.time_controller import TimeController
from src.app.items.fruits.fruit_factory import FruitFactory
from src.config import FruitConfig, APPLE_IMG_PATH, ORANGE_IMG_PATH, PEACH_IMG_PATH


class ItemsSpawner:
    def __init__(self, fruits_config, bomb_config, time_controller, init_difficulty):
        self.time_controller = time_controller
        self.fruits_config = fruits_config
        self.bomb_config = bomb_config
        self._interval = 1  # seconds
        self._items_to_spawn = []
        self._intensity = init_difficulty

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, new_interval):
        self._interval = new_interval

    @property
    def intensity(self):
        return self._intensity

    @intensity.setter
    def intensity(self, new_intensity):
        self._intensity = new_intensity

    def update(self):
        if TimeController.get_interval_since_last_spawn >= self._interval:
            # TODO BASED ON intensity PROPERTY
            # tu losuje ile itemków
            # tu losuje jakie itemki

            # temporary solution - spawning 2 items at once
            self._items_to_spawn = [1, 1, 1]

            for item in self._items_to_spawn:
                self.spawn_item(item)

            self.time_controller.update_last_spawn_time()

    def spawn_item(self, item):
        # TODO spawn fruit based on item in the argument
        fruit_config = FruitConfig(
            10, APPLE_IMG_PATH, FruitType.APPLE, 2
        )
        FruitFactory.create(fruit_config, Vector2(randint(200, 600), 400), Vector2(randint(-5, 5), -randint(12, 17)))
