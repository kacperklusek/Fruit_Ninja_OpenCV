import time
import pygame
from pygame import Surface
from pygame.color import Color
from pygame.math import Vector2
from pygame.sprite import Sprite, Group
from typing import Union
from collections import deque
from src.app.utils.timeouts import Interval
from threading import Lock
from src.config import effects_config
from src.app.effects.animations import Animation, KeyFrame, alpha_animation


class TrailPart:
    DISPLAY_DURATION = .5

    def __init__(self, position: Vector2, size: Union[int, float], color: Color, max_alpha: int):
        self.position = Vector2(position)
        self.color = color
        self.initial_size = size
        self.initial_alpha = color.a
        self.max_alpha = max_alpha
        self.creation_time = time.time()
        self.size = size

    @property
    def x(self):
        return self.position.x

    @property
    def y(self):
        return self.position.y

    def blit(self, surface):  # TODO - maybe make common abstract class not only for Menu Elements but also for other objects like this (with the abstract blit method)
        self.update()
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.size)

    def update(self):
        elapsed_time = time.time() - self.creation_time
        ratio = 1 - elapsed_time / self.DISPLAY_DURATION
        self.size = ratio * self.initial_size
        alpha = min(max(int(self.initial_alpha + ratio * (self.max_alpha - self.initial_alpha)), 0), 255)
        r, g, b, _ = self.color
        self.color.update(r, g, b, alpha)


class Trail(Sprite):
    def __init__(self, item, group: Group, size: Union[float, int] = -1):
        Sprite.__init__(self)
        self.group = group
        self.item = item
        self.size = size if size > 0 else min(item.width, item.height) / 3
        self.parts = deque()
        self.mutex = Lock()
        self.interval = Interval(self.__add_part, effects_config.ITEM_TRAIL_SPAWN_INTERVAL, self.mutex)

        # Dummy variables required by the Sprite class
        self.image = Surface((0, 0))
        self.rect = self.image.get_rect()
        group.add(self)

    def blit(self, surface):
        self.mutex.acquire(True)
        for part in self.parts:
            part.blit(surface)
        self.mutex.release()

    def update(self, **kwargs):
        if self.item.is_killed:
            self.remove()
            return

        while self.parts and self.parts[0].size <= 0:
            self.parts.popleft()
            # Add the new trail part if the interval is finished
            if not self.interval:
                self.__add_part()

        self.blit(kwargs['surface'])

    def remove(self):
        if self.interval:
            self.interval.clear()
        self.parts.clear()
        self.group.remove(self)

    def __add_part_interval(self):
        if len(self.parts) < effects_config.ITEM_TRAIL_PARTS_COUNT:
            self.__add_part()
        else:
            self.interval.clear()
            self.interval = None

    def __add_part(self):
        self.parts.append(TrailPart(
            self.item.position,
            self.size,
            effects_config.ITEM_TRAIL_COLOR,
            effects_config.ITEM_TRAIL_MAX_ALPHA
        ))


class Splash(Sprite):
    def __init__(self, image, position: Vector2, group: Group):
        Sprite.__init__(self)
        self.original_image = image
        self.image = image
        self.position = position
        self.group = group
        self.alpha = effects_config.SPLASH_ALPHA

        self.animation = Animation(self, [
            KeyFrame(0, None),
            KeyFrame(.75, alpha_animation(self.alpha, 0))
        ], effects_config.SPLASH_VISIBILITY_DURATION)
        self.group.add(self)

    @property
    def rect(self):
        return self.image.get_rect(center=self.position)

    def update(self, *args, **kwargs):
        if not self.animation.started:
            self.animation.start()

        self.image.set_alpha(self.alpha)
        if self.animation.finished:
            self.group.remove(self)
