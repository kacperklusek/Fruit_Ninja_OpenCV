import pygame
from pygame.math import Vector2
from ..physics.gravity_controller import GravityController


class Item(pygame.sprite.Sprite):
    gravity_controller = GravityController(Vector2(0, 2))

    def __init__(self, position: Vector2, velocity: Vector2 = Vector2(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.velocity = velocity
        self.position = position

    def update(self):
        self.apply_gravity()

    def apply_gravity(self):
        self.velocity += self.gravity_controller
        self.position += self.velocity
