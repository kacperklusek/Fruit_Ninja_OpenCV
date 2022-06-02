import pygame.transform
from pygame.sprite import Sprite, Group
from pygame import Vector2
from pygame.font import Font
from pygame.surface import SurfaceType, Surface
from src.app.gui.common import MenuElement, KeyFrame, Animation
from src.config import game_config, effects_config


class Label(MenuElement):
    def __init__(self, text: Surface | SurfaceType, position: Vector2):
        self.text = text
        self.position = position

    @property
    def rect(self):
        return self.text.get_rect(center=self.position)

    def blit(self, surface):
        surface.blit(self.text, self.position)


def scale_animation(from_scale, to_scale, animation_timing_function=lambda x: x):
    def apply_to(element, percent):
        percent = animation_timing_function(percent)
        element.scale = abs(to_scale - from_scale) * (percent if to_scale > from_scale else 1 - percent)
    return apply_to


class ComboLabel(Sprite):
    def __init__(self, combo_value: int, position: Vector2, group: Group):
        Sprite.__init__(self)
        self.font = Font(game_config.FONT, effects_config.COMBO_FONT_SIZE)
        self.combo_text = self.font.render(f'COMBO +{combo_value}', True, 'White')
        self.animation_start_time = 0
        self.position = position
        self.image = self.combo_text
        self.group = group
        group.add(self)

        timing_function = lambda x: x ** 3

        self.animation = Animation(self, effects_config.COMBO_DISPLAY_DURATION, [
            KeyFrame(0, scale_animation(0, 1, timing_function)),
            KeyFrame(.2, None),
            KeyFrame(.8, scale_animation(1, 0, timing_function))
        ])
        self.scale = 0
        self.animation_started = False

    @property
    def rect(self):
        return self.image.get_rect(center=self.position)

    def update(self):
        if not self.animation_started:
            self.animation.start()
            self.animation_started = True
        if self.animation.finished:
            self.group.remove(self)
            self.kill()

        rect = self.combo_text.get_rect()
        self.image = pygame.transform.scale(self.combo_text, (self.scale * rect.width, self.scale * rect.height))
