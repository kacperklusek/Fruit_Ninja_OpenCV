import pygame
from pygame.math import Vector2

from src.app.physics.gravity_controller import GravityController

from src.config import game_config


class Item(pygame.sprite.Sprite):
    gravity_controller = GravityController(Vector2(0, 10))
    out_of_bounds = 0

    def __init__(self, image: str, position: Vector2, velocity: Vector2 = Vector2(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.velocity = velocity
        self.position = position
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = position.x
        self.rect.y = position.y

    def update(self, elapsed_time):
        self.apply_gravity(elapsed_time)
        self.check_screen_boundaries()

    def apply_gravity(self, elapsed_time):
        self.velocity += self.gravity_controller.g * elapsed_time  # 0.016 * 60 = 1
        self.position += self.velocity * elapsed_time
        self.rect.x = self.position.x
        self.rect.y = self.position.y

    def check_screen_boundaries(self):
        if self.position.y > game_config.HEIGHT + 100 and self.velocity.y > 0:
            self.handle_out_of_bounds()

    def handle_out_of_bounds(self):
        self.kill()
        Item.out_of_bounds += 1
