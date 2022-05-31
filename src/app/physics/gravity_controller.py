from pygame.math import Vector2
from src.app.utils.design_patterns import Singleton


class GravityController(metaclass=Singleton):
    def __init__(self):
        self.__g = Vector2(0, 0)

    @property
    def gravity(self):
        return self.__g

    @gravity.setter
    def gravity(self, new_gravity: Vector2):
        self.__g = new_gravity
