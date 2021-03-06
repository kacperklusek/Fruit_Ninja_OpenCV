from src.app.controllers.input_controller import FingerInput, HandInput, MouseInput
from src.config import blade_config as config
from src.app.utils.enums import InputSource
from src.app.utils.point import Point
from src.config import window_config
import pygame


class Blade(pygame.sprite.Sprite):
    EMPTY_COLOR = pygame.Color(0, 0, 0, 0)
    BLADE_WIDTH = 5

    def __init__(self, game, input_source):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.input_source = self.create_input_source(input_source)
        self.input_source.start_tracking()
        self._blade_surface = pygame.Surface((window_config.WIDTH, window_config.HEIGHT), pygame.SRCALPHA)
        self._collision_enabled = True

    def __len__(self):
        return len(self.input_source.points_history)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.points_history})'

    def __getitem__(self, idx):
        return self.points_history[idx]

    def enable_collision(self):
        self._collision_enabled = True

    def disable_collision(self):
        self._collision_enabled = False

    @property
    def points_history(self):
        if isinstance(self.input_source, MouseInput):
            return self.input_source.points_history
        else:
            result = []
            history = self.input_source.points_history
            if history: result.append(history[0])

            for i in range(1, len(history)):
                x = (history[i].x + history[i - 1].x) / 2
                y = (history[i].y + history[i - 1].y) / 2
                result.append(Point(x, y))
                result.append(history[i])
            return result

    def destroy(self):
        self.input_source.end_tracking()

    def draw(self):
        self._blade_surface.fill(self.EMPTY_COLOR)
        points = self.points_history[:]
        if len(points) > 1:
            pygame.draw.lines(self._blade_surface, config.COLORS[0], False, points, self.BLADE_WIDTH)
        self.game.screen.blit(self._blade_surface, (0, 0))

    def change_input_source(self, input_source_type):
        self.input_source.end_tracking()
        self.input_source = self.create_input_source(input_source_type)

    def clear(self):
        self.input_source.clear_history()

    @staticmethod
    def create_input_source(input_source_type):
        match input_source_type:
            case InputSource.HAND:
                return HandInput()
            case InputSource.FINGER:
                return FingerInput()
            case InputSource.MOUSE:
                return MouseInput()

    def collides(self, obj):
        if not self._collision_enabled:
            return False
        return any(map(obj.rect.collidepoint, self.input_source.get_points_for_collision()))
