from src.app.items.fruits.fruit_type import FruitType
from src.app.items.fruits.fruit import Fruit
from pygame.math import Vector2


class FruitFactory:
    @staticmethod
    def create(fruit_config, position: Vector2, velocity: Vector2):
        match fruit_config.FRUIT_TYPE:
            case FruitType.APPLE | FruitType.ORANGE:
                return Fruit(fruit_config, position, velocity)
            case FruitType.FREEZE_BANANA:
                ...
