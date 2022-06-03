from src.app.utils.singleton import SingletonMeta
from pygame.math import Vector2


class GravityController(metaclass=SingletonMeta):
    def __init__(self, initial_gravity: Vector2 = None):
        self._g = initial_gravity

    @property
    def gravity(self):
        return self._g

    @gravity.setter
    def gravity(self, new_gravity: Vector2):
        self._g = new_gravity
