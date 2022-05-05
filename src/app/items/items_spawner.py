import random
from time import time
from pygame.math import Vector2
from random import randint
from src.app.utils.enums.items import ItemType
from src.app.items.item_factory import ItemFactory


class ItemsSpawner:
    BONUS_FRUIT_CHANCE = 0.1

    def __init__(self, init_difficulty):
        self._interval = 2  # seconds
        self._items_to_spawn = []
        self._intensity = init_difficulty
        self.last_spawn_time = 0

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
            return random.choice([
                ItemType.FREEZE_FRUIT,
                ItemType.GRAVITY_FRUIT
            ])
        else:
            return ItemType.PLAIN_FRUIT

    def update(self):
        curr_time = time()
        if curr_time - self.last_spawn_time >= self._interval:
            self._items_to_spawn = [self.choose_fruit_type() for _ in range(int(self._intensity))]

            for fruit_type in self._items_to_spawn:
                self.spawn_item(fruit_type)

            self.last_spawn_time = curr_time

    @staticmethod
    def spawn_item(fruit_type):
        # TODO spawn fruit based on item in the argument
        # FruitFactory.create(fruit_config, Vector2(randint(200, 600), 400), Vector2(randint(-5, 5), -randint(12, 17)))
        item = ItemFactory.create(fruit_type)
        item.spawn(Vector2(randint(200, 600), 400), Vector2(randint(-100, 100), -randint(500, 700)))
