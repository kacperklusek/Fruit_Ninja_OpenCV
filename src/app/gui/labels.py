import pygame.transform
from pygame import Vector2
from pygame.font import Font
from pygame.surface import SurfaceType, Surface
from src.app.gui.common import MenuElement, KeyFrame, Animation
from src.config import game_config


class Label(MenuElement):
    def __init__(self, text: Surface | SurfaceType, position: Vector2):
        self.text = text
        self.position = position

    @property
    def rect(self):
        return self.text.get_rect(center=self.position)

    def blit(self, surface):
        surface.blit(self.text, self.position)


def scale_animation(from_scale, to_scale):
    def apply_to(element, percent):
        element.scale = abs(to_scale - from_scale) * (percent if to_scale > from_scale else 1 - percent)
    return apply_to


class ComboLabel(Label):
    VISIBILITY_DURATION = 1
    TRANSITION_DURATION = .25

    def __init__(self, combo_value: int, position: Vector2):
        self.font = Font(game_config.FONT, game_config.FONT_SIZE)
        self.combo_text = self.font.render(f'COMBO X{combo_value}', True, 'White')
        Label.__init__(self, self.combo_text, position)
        self.animation_start_time = 0
        self.scale = 0

        self.animation = Animation(self, self.VISIBILITY_DURATION, [
            KeyFrame(0, scale_animation(0, 1)),
            KeyFrame(.25, None),
            KeyFrame(.75, scale_animation(1, 0))
        ])
        self.animation_started = False
        self.animated_text = self.text

    def blit(self, surface):
        self.update()
        surface.blit(self.animated_text, self.position)

    def update(self):
        if not self.animation_started:
            self.animation.start()
            self.animation_started = True
        rect = self.text.get_rect()
        self.animated_text = pygame.transform.scale(self.text, (self.scale * rect.width, self.scale * rect.height))
