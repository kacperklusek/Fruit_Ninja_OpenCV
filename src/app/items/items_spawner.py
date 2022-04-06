from pygame.math import Vector2

from src.app.items.bombs.bomb import Bomb
from src.app.items.fruits.fruit import Fruit


class ItemsSpawner:
    @staticmethod
    def spawn_fruit(position: Vector2, velocity: Vector2 = Vector2(0, 0)):
        # TODO - add spawning different fruit types
        return Fruit('Apple', position, velocity)

    @staticmethod
    def spawn_bomb(position: Vector2, velocity: Vector2 = Vector2(0, 0)):
        return Bomb()  # TODO - implement Bomb class
