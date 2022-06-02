import random
from time import time

from abc import ABC, abstractmethod
from pygame import Vector2

from src.config import window_config
from src.app.utils.enums import ItemType
from src.app.items.item_factory import ItemFactory
from src.app.controllers.gravity_controller import GravityController
from src.app.effects.sounds import SoundController
from pygame.sprite import Group


class ItemSpawner(ABC):
    BONUS_FRUIT_CHANCE = 0.1

    def __init__(self, fruits: Group, bombs: Group, callback):
        self.fruits = fruits
        self.bombs = bombs
        self.callback = callback

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def spawn_item(self, item_type: ItemType):
        pass


class ClassicModeItemSpawner(ItemSpawner):
    def __init__(self, fruits: Group, bombs: Group, callback):
        ItemSpawner.__init__(self, fruits, bombs, callback)

        self._interval = 2  # seconds
        self._items_to_spawn = []
        self._intensity = 2
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

    def choose_item_type(self):
        if int(random.random() * (1 + self.BONUS_FRUIT_CHANCE)) == 1:
            return random.choice([
                ItemType.BOMB,
                ItemType.BOMB
            ])
        else:
            return ItemType.PLAIN_FRUIT

    def update(self):
        curr_time = time()
        if curr_time - self.last_spawn_time >= self._interval:
            self._items_to_spawn = [self.choose_item_type() for _ in range(int(self._intensity))]

            for item_type in self._items_to_spawn:
                self.spawn_item(item_type)

            self.last_spawn_time = curr_time

    def spawn_item(self, item_type: ItemType):
        match item_type:
            case ItemType.PLAIN_FRUIT:
                item = ItemFactory.create(item_type, self.fruits)
            case ItemType.BOMB:
                item = ItemFactory.create(item_type, self.bombs)
            case _:
                raise ValueError(f'{item_type} is not a valid item type')

        # TODO - refactor code below
        x = window_config.WIDTH * (random.random() * .5 + .25)
        v_x = random.randint(-window_config.WIDTH // 10, window_config.WIDTH // 10)
        v_y = random.randint(1.2 * window_config.HEIGHT, int(1.5 * window_config.HEIGHT))

        if self.gravity_controller.gravity.y > 0:
            item.throw(Vector2(x, 1.1 * window_config.HEIGHT), Vector2(v_x, -v_y))
        else:
            item.throw(Vector2(x, -.1 * window_config.HEIGHT), Vector2(v_x, v_y))

        SoundController.play_throw_sound()
        self.callback(item)

    def set_interval(self, interval):
        self._interval = interval

    def set_intensity(self, intensity):
        self._intensity = intensity
