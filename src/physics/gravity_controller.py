from pygame.math import Vector2


class GravityController:
    a = 1

    def __init__(self, g: Vector2):
        self.g = g
