import pygame
import random
from pygame.math import Vector2
from pygame.sprite import Sprite, Group
from src.config import window_config, game_config
from src.app.utils.image_loader import ImageLoader
from src.app.controllers.time_controller import TimeController
from src.app.controllers.gravity_controller import GravityController


class Item(Sprite):
    def __init__(self, image_path: str, group: Group):
        Sprite.__init__(self)
        self.image_path = image_path
        self.gravity_controller = GravityController()
        self.time_controller = TimeController()
        self.velocity = Vector2(0, 0)
        self.position = Vector2(0, 0)
        self.original_image = ImageLoader.load_png(self.image_path, -1, game_config.ITEM_SIZE)
        self.image = self.original_image
        self.angular_velocity = 0
        self.angle = 0
        self.group = group
        self.is_killed = False

        self.observers = []

    def add_observer(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def notify_item_killed(self):
        for observer in self.observers:
            observer.item_killed()

    @property
    def rect(self):
        return self.image.get_rect(center=self.position)

    @property
    def width(self):
        return self.image.get_width()

    @property
    def height(self):
        return self.image.get_height()

    def throw(self, position: Vector2, velocity=Vector2(0, 0), angle=None, angular_velocity=None):
        self.group.add(self)
        self.angle = angle or random.randint(0, 360)
        self.angular_velocity = angular_velocity or random.random() - .5
        self.position = position
        self.velocity = velocity
        self.update_position()

    def kill(self):
        self.is_killed = True
        self.group.remove(self)
        Sprite.kill(self)
        self.notify_item_killed()

    def update(self, **kwargs):
        self.rotate()
        self.update_position()

        if self.item_out_of_bounds():
            if 'out_of_bounds_handler' in kwargs:
                kwargs['out_of_bounds_handler']()
            self.kill()
            return

    def update_position(self):
        elapsed_time = self.time_controller.last_frame_duration
        self.velocity += self.gravity_controller.gravity * elapsed_time
        self.position += self.velocity * elapsed_time
        self.rect.x = self.position.x - self.image.get_width() / 2
        self.rect.y = self.position.y - self.image.get_height() / 2

    def rotate(self):
        self.angle = (self.angle + self.angular_velocity) % 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)

    def item_out_of_bounds(self):
        gravity_y = self.gravity_controller.gravity.y
        return (gravity_y > 0 and self.position.y > window_config.HEIGHT and self.velocity.y > 0) \
            or (gravity_y < 0 and self.position.y < 0 and self.velocity.y < 0)
