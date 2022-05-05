import pygame
from src.config import blade_config as config
from src.app.utils.enums.input_source import InputSource
from src.app.control.input_controller import FingerInput, HandInput, MouseInput


class Blade(pygame.sprite.Sprite):
    EMPTY_COLOR = pygame.Color(0, 0, 0, 0)
    APPROXIMATION_POINTS = 100

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
        print(self.input_source.points_history)
        return self.input_source.points_history

    def draw(self):
        self.surface.fill(self.EMPTY_COLOR)
        points = self.points_history[:]
        if len(points) > 1:
            pygame.draw.lines(self.surface, config.COLORS[0], False, points, len(self))
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
