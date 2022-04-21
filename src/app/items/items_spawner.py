from pygame.math import Vector2
from random import randint
import math

from src.app.items.bombs.bomb import Bomb
from src.app.items.fruits.fruit import Fruit
from src.app.enums.fruit_type import FruitType


class ItemsSpawner:
    def __init__(self, fruit_frequency, bomb_frequency):
        self.fruit_frequency = fruit_frequency
        self.bomb_frequency = bomb_frequency
        self.lcm = math.lcm(fruit_frequency, bomb_frequency)
        self.frames = self.lcm

    def handle_spawning(self):
        self.frames -= 1
        if self.frames == 0:
            self.frames = self.lcm
        if self.frames % self.fruit_frequency == 0:
            self.spawn_fruit(Vector2(randint(200, 600), 400), Vector2(randint(-5, 5), -randint(12, 17)))
        if self.frames % self.bomb_frequency == 0:
            self.spawn_bomb(Vector2(randint(200, 600), 400), Vector2(randint(-5, 5), -randint(12, 17)))

    @staticmethod
    def spawn_fruit(position: Vector2, velocity: Vector2 = Vector2(0, 0)):
        # TODO - add spawning different fruit types
        Fruit(FruitType.Apple, position, velocity)

    @staticmethod
    def spawn_bomb(position: Vector2, velocity: Vector2 = Vector2(0, 0)):
        Bomb(position, velocity)

