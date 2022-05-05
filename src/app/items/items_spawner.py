import random

from pygame.math import Vector2

from random import randint

from src.app.items.bombs.bomb import Bomb
from src.app.items.fruits.fruit import Fruit
from src.app.items.fruits.fruit_type import FruitType
from src.app.physics.time_controller import TimeController
from src.app.items.fruits.fruit_factory import FruitFactory
from src.app.items.fruits.fruit_type import FruitType


class ItemsSpawner:
    BONUS_FRUIT_CHANCE = 0.1

    def __init__(self, fruits_config, bomb_config, time_controller, init_difficulty):
        self.fruit_factory = FruitFactory(fruits_config)
        self.time_controller = time_controller
        self.fruits_config = fruits_config
        self.bomb_config = bomb_config
        self._interval = 2  # seconds
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
    def intensity(self, intensity):
        self._intensity = intensity

    def choose_fruit_type(self):
        if int(random.random() * (1 + self.BONUS_FRUIT_CHANCE)) == 1:
            return FruitType.BONUS
        else:
            return FruitType.PLAIN

    def update(self):
        if TimeController.get_interval_since_last_spawn >= self._interval:
            self._items_to_spawn = [self.choose_fruit_type() for _ in range(int(self._intensity))]

            for fruit_type in self._items_to_spawn:
                self.spawn_item(fruit_type)

            self.time_controller.update_last_spawn_time()

    def spawn_item(self, fruit_type):
        # TODO spawn fruit based on item in the argument
        # FruitFactory.create(fruit_config, Vector2(randint(200, 600), 400), Vector2(randint(-5, 5), -randint(12, 17)))
        self.fruit_factory.create(FruitType.PLAIN,
                            Vector2(randint(200, 600), 400),
                            Vector2(randint(-100, 100), -randint(500, 700)))
