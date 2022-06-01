import pygame
from src.config import blade_config as config
from src.app.utils.enums import InputSource
from src.app.control.input_controller import FingerInput, HandInput, MouseInput, InputPoint
from src.app.utils.point import Point
from src.config import game_config


class Blade(pygame.sprite.Sprite):
    EMPTY_COLOR = pygame.Color(0, 0, 0, 0)
    BLADE_WIDTH = 5

    def __init__(self, screen, input_source):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.input_source = self.create_input_source(input_source)
        self.surface = pygame.Surface((screen.get_width(), screen.get_height()), flags=pygame.SRCALPHA)
        self.input_source.start_tracking()

    def __len__(self):
        return len(self.input_source.points_history)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.points_history})'

    def __getitem__(self, idx):
        return self.points_history[idx]

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
        self.surface.fill(self.EMPTY_COLOR)
        points = self.points_history[:]
        if len(points) > 1:
            pygame.draw.lines(self.surface, config.COLORS[0], False, points, self.BLADE_WIDTH)
            for point in points:
                pygame.draw.circle(self.surface, 'red', point, 4)  # TODO - remove this line after
            self.screen.blit(self.surface, (0, 0))

    def change_input_source(self, input_source_type):
        self.input_source.end_tracking()
        self.input_source = self.create_input_source(input_source_type)

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
        return any(map(obj.rect.collidepoint, self[-1 if game_config.INPUT_SOURCE == InputSource.MOUSE else 5:]))
