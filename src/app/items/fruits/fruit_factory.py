import random
from src.app.items.fruits.fruit_type import FruitType
from src.app.items.fruits.fruit import PlainFruit
from pygame.math import Vector2


class FruitFactory:
    def __init__(self, config):
        self.config = config

    def create(self, fruit_type, position: Vector2, velocity: Vector2):
        match fruit_type:
            case FruitType.PLAIN:
                return PlainFruit(random.choice(self.config.PLAIN.IMAGE_PATHS), position, velocity)
            case FruitType.BONUS:
                ...
