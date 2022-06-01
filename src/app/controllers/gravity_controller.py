from pygame.math import Vector2
from src.app.utils.singleton import SingletonMeta


class GravityController(metaclass=SingletonMeta):
    def __init__(self, initial_gravity: Vector2 = None):
        self.__g = initial_gravity

    @property
    def gravity(self):
        return self.__g

    @gravity.setter
    def gravity(self, new_gravity: Vector2):
        self.__g = new_gravity
