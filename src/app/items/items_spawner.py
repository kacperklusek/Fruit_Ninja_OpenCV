import random
from time import time

from pygame import Vector2

from src.config import window_config
from src.app.utils.enums.items import ItemType
from src.app.items.item_factory import ItemFactory
from src.app.physics.gravity_controller import GravityController


class ItemsSpawner:
    BONUS_FRUIT_CHANCE = 0.1

    def __init__(self, init_difficulty):
        self._interval = 2  # seconds
        self._items_to_spawn = []
        self._intensity = init_difficulty
        self.last_spawn_time = 0
        self.gravity_controller = GravityController()

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

    def spawn_item(self, fruit_type):
        # FruitFactory.create(fruit_config, Vector2(randint(200, 600), 400), Vector2(randint(-5, 5), -randint(12, 17)))
        item = ItemFactory.create(fruit_type)

        print(self.gravity_controller.gravity)

        x = window_config.WIDTH * (random.random() * .5 + .25)
        v_x = random.randint(-window_config.WIDTH // 10, window_config.WIDTH // 10)
        v_y = random.randint(1.2 * window_config.HEIGHT, int(1.5 * window_config.HEIGHT))

        if self.gravity_controller.gravity.y > 0:
            item.spawn(Vector2(x, 1.1 * window_config.HEIGHT), Vector2(v_x, -v_y))
        else:
            item.spawn(Vector2(x, -.1 * window_config.HEIGHT), Vector2(v_x, v_y))
