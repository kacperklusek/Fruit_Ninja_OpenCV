import time
import random
from collections import deque
from typing import Union

from pygame import Vector2

from src.app.items.item import Item
from src.config import window_config
from src.app.utils.enums import ItemType
from src.app.items.item_factory import ItemFactory
from src.app.effects.sounds import SoundController
from pygame.sprite import Group


class ItemToSpawn:
    def __init__(self, item: Item, position: Vector2, velocity: Vector2, delay: Union[int, float]):
        self.item = item
        self.delay = delay

        self.position = position
        self.velocity = velocity

        self.creation_time = time.time()

    @property
    def spawn_time(self):
        return self.creation_time + self.delay

    def can_be_spawned(self):
        return time.time() - self.creation_time > self.delay

    def throw(self):
        SoundController.play_throw_sound()
        self.item.throw(self.position, self.velocity)


class ItemSpawner:
    BONUS_FRUIT_CHANCE = 0.1

    def __init__(self, fruits: Group, bombs: Group, callback):
        self.fruits = fruits
        self.bombs = bombs
        self.callback = callback
        self.last_spawn_time = 0
        self.create_items_methods = []
        self.items_to_spawn = deque()
        self._interval = 2  # TODO - change these variables
        self._intensity = 1  # TODO - change these variables

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, interval: Union[int, float]):
        self._interval = interval

    @property
    def intensity(self):
        return self._intensity

    @intensity.setter
    def intensity(self, intensity: Union[int, float]):
        self._intensity = intensity

    def update(self):
        curr_time = time.time()
        self.spawn_items()
        if curr_time - self.last_spawn_time > self.interval:
            print('create')
            self.create_items_to_spawn()
            if self.items_to_spawn:
                self.last_spawn_time = self.items_to_spawn[-1].spawn_time

    def spawn_items(self):
        while self.items_to_spawn and self.items_to_spawn[0].can_be_spawned():
            item = self.items_to_spawn.popleft()
            item.throw()
            self.callback(item.item)

    def create_items_to_spawn(self):
        random.choice(self.create_items_methods)()


class ClassicModeItemSpawner(ItemSpawner):
    MIN_SPAWN_X = .25 * window_config.WIDTH
    MAX_SPAWN_X = .75 * window_config.WIDTH

    def __init__(self, fruits: Group, bombs: Group, callback):
        ItemSpawner.__init__(self, fruits, bombs, callback)

        self.create_items_methods.extend([
            self.create_multiple,
            self.create_sequence
        ])

        self._bomb_probability = 0

    @property
    def bomb_probability(self):
        return self._bomb_probability

    @bomb_probability.setter
    def bomb_probability(self, bomb_probability: float):
        if not 0 < bomb_probability < 1:
            raise ValueError(f'Bomb probability must be between 0 and 1')
        self._bomb_probability = bomb_probability

    def create_multiple(self):
        self._create_sequence_helper(0, 0)
        # Spawn bomb with a delay
        if random.random() < self.bomb_probability:
            # Spawn max 2 bombs when throwing multiple fruits at once
            delays = sorted([.5 + random.random() / 2 for _ in range(random.randint(1, 2))])
            for delay in delays:
                self.items_to_spawn.append(self._create_item_to_spawn(delay, 1))

    def create_sequence(self):
        min_delay = max(int(self.interval / 8), 1)
        max_delay = max(int(self.interval / 3), 1)
        self._create_sequence_helper(random.randint(min_delay, max_delay), self.bomb_probability)

    def _create_sequence_helper(self, delay, bomb_probability):
        bomb_probability = bomb_probability if random.random() < .75 else 0
        for i in range(max(random.randint(int(self.intensity // 2), int(self.intensity)), 1)):
            item_to_spawn = self._create_item_to_spawn(i * delay, bomb_probability)
            self.items_to_spawn.append(item_to_spawn)

    def _create_item_to_spawn(self, delay, bomb_probability):
        item_type = ItemType.PLAIN_FRUIT if random.random() > bomb_probability else ItemType.BOMB
        item = ItemFactory.create(item_type, self.bombs if item_type is ItemType.BOMB else self.fruits)
        x = random.randint(self.MIN_SPAWN_X, self.MAX_SPAWN_X)
        ratio = (x - self.MIN_SPAWN_X) / (self.MAX_SPAWN_X - self.MIN_SPAWN_X) - .5
        v_x = int(-ratio * random.random() * window_config.WIDTH)
        v_y = -random.randint(int(1.2 * window_config.HEIGHT), int(1.5 * window_config.HEIGHT))
        position = Vector2(x, 1.1 * window_config.HEIGHT)
        velocity = Vector2(v_x, v_y)

        return ItemToSpawn(item, position, velocity, delay)
