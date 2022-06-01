import pygame
from pygame.sprite import Sprite
import random
from pygame.math import Vector2
from src.app.controllers.gravity_controller import GravityController
from src.config import window_config
from src.app.utils.image_loader import ImageLoader
from src.app.effects.visual import TrailShadow


class Item(Sprite):
    out_of_bounds = 0

    def __init__(self, image: str):  # TODO - think what to do with this surface
        Sprite.__init__(self)
        self.gravity_controller = GravityController()
        self.velocity = Vector2(0, 0)
        self.position = Vector2(0, 0)
        self.original_image = ImageLoader.load_png(image, 100)
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = self.image.get_rect().center
        self.rect.x = 0
        self.rect.y = 0
        self.rotation_speed = (random.random() - 0.5)
        self.angle = random.randint(0, 360)
        self.trail_shadow = None

    @property
    def width(self):
        return self.image.get_width()

    @property
    def height(self):
        return self.image.get_height()

    def spawn(self, position, velocity=Vector2(0, 0)):
        self.position = position
        self.velocity = velocity
        self.update_position()
        self.trail_shadow = TrailShadow(self)

    def update(self, elapsed_time):
        self.rotate()
        self.apply_gravity(elapsed_time)
        self.check_screen_boundaries()
        self.update_position()

    def apply_gravity(self, elapsed_time):
        self.velocity += self.gravity_controller.gravity * elapsed_time
        self.position += self.velocity * elapsed_time

    def update_position(self):
        self.rect.x = self.position.x - self.image.get_width() / 2
        self.rect.y = self.position.y - self.image.get_height() / 2

    def rotate(self):
        self.angle = (self.angle + self.rotation_speed) % 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)

    def check_screen_boundaries(self):
        if (self.gravity_controller.gravity.y > 0 and self.position.y > window_config.HEIGHT and self.velocity.y > 0) \
                or (self.gravity_controller.gravity.y < 0 and self.position.y < 0 and self.velocity.y < 0):
            self.handle_out_of_bounds()

    def handle_out_of_bounds(self):
        self.kill()
        Item.out_of_bounds += 1

    @classmethod
    def reset(cls):
        cls.out_of_bounds = 0

