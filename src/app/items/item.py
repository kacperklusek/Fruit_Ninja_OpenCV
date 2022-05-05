import pygame
import random
from pygame.math import Vector2
from src.app.physics.gravity_controller import GravityController
from src.config import window_config


class Item(pygame.sprite.Sprite):
    gravity_controller = GravityController(Vector2(0, 600))
    out_of_bounds = 0

    def __init__(self, image: str):
        pygame.sprite.Sprite.__init__(self)
        self.velocity = Vector2(0, 0)
        self.position = Vector2(0, 0)
        self.original_image = pygame.image.load(image).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (100, 100))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = self.image.get_rect().center
        self.rect.x = 0
        self.rect.y = 0
        self.rotation_speed = (random.random() - 0.5)
        self.angle = random.randint(0, 360)

    def spawn(self, position, velocity=Vector2(0, 0)):
        self.position = position
        self.velocity = velocity
        self.update_position()

    def update(self, elapsed_time):
        self.rotate()
        self.apply_gravity(elapsed_time)
        self.check_screen_boundaries()
        self.update_position()

    def apply_gravity(self, elapsed_time):
        self.velocity += self.gravity_controller.g * elapsed_time
        self.position += self.velocity * elapsed_time

    def update_position(self):
        self.rect.x = self.position.x - self.image.get_width() / 2
        self.rect.y = self.position.y - self.image.get_height() / 2

    def rotate(self):
        self.angle = (self.angle + self.rotation_speed) % 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)

    def check_screen_boundaries(self):
        if self.position.y > window_config.HEIGHT + 100 and self.velocity.y > 0:
            self.handle_out_of_bounds()

    def handle_out_of_bounds(self):
        self.kill()
        Item.out_of_bounds += 1
