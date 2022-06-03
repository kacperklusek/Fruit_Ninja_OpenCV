import pygame.transform
from typing import Union
from pygame.sprite import Sprite, Group
from pygame.math import Vector2
from pygame.surface import SurfaceType, Surface

from src.app.effects.animations import Animation, KeyFrame, scale_animation, cubic_timing
from src.app.gui.common import MenuElement


class Label(MenuElement):
    def __init__(self, text: Surface | SurfaceType, position: Vector2):
        self.text = text
        self.position = position

    @property
    def rect(self):
        return self.text.get_rect(center=self.position)

    def blit(self, surface):
        surface.blit(self.text, self.position)


class AnimatedLabel(Sprite):
    def __init__(self, text_lines, position: Vector2, display_duration: Union[float, int], group: Group):
        Sprite.__init__(self)
        self.surface = self._create_label(text_lines)
        self.image = self.surface
        self.animation_start_time = 0
        self.position = position
        self.group = group
        group.add(self)

        self.animation = Animation(self, [
            KeyFrame(0, scale_animation(0, 1, cubic_timing)),
            KeyFrame(.2, None),
            KeyFrame(.8, scale_animation(1, 0, cubic_timing))
        ], display_duration)
        self.scale = 0

    @property
    def rect(self):
        return self.image.get_rect(center=self.position)

    def update(self):
        if not self.animation.started:
            self.animation.start()
        if self.animation.finished:
            self.group.remove(self)
            self.kill()

        rect = self.surface.get_rect()
        self.image = pygame.transform.scale(self.surface, (self.scale * rect.width, self.scale * rect.height))

    @staticmethod
    def _create_label(text_lines):
        width = max(line.get_width() for line in text_lines)
        height = sum(line.get_height() for line in text_lines)
        surface = Surface((width, height), pygame.SRCALPHA)

        curr_height = 0
        for line in text_lines:
            surface.blit(line, (0, curr_height))
            curr_height += line.get_height()

        return surface
