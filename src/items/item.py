import pygame
from pygame.math import Vector2
from physics.gravity_controller import GravityController


class Item(pygame.sprite.Sprite):
    gravity_controller = GravityController(Vector2(0, 2))

    def __init__(self, image: str, position: Vector2, velocity: Vector2 = Vector2(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.velocity = velocity
        self.position = position
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = position.x
        self.rect.y = position.y

    def update(self):
        self.apply_gravity()

    def apply_gravity(self):
        self.velocity += self.gravity_controller.g
        self.position += self.velocity
        self.rect.x = self.position.x
        self.rect.y = self.position.y
