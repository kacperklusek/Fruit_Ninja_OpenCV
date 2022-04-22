import pygame
import numpy as np
from src.app.enums.input_source import InputSource
from src.app.input.input_source import FingerInput, HandInput, MouseInput


class Blade(pygame.sprite.Sprite):  # TODO - replace line drawing from main with instance of this class
    EMPTY_COLOR = pygame.Color(0, 0, 0, 0)
    APPROXIMATION_POINTS = 100

    def __init__(self, config, screen):
        pygame.sprite.Sprite.__init__(self)
        self.config = config
        self.screen = screen
        self.input_source = self.create_input_source(input_source_type=config.INPUT_SOURCE)
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
        return self.input_source.points_history

    def draw(self):
        self.surface.fill(self.EMPTY_COLOR)
        if len(self.points_history) > 1:
            # points = self.approximate_points()
            pygame.draw.lines(self.surface, self.config.COLORS[0], False, self.points_history, len(self))
            self.screen.blit(self.surface, (0, 0))

    def change_input_source(self, input_source_type):
        self.input_source.end_tracking()
        self.input_source = self.create_input_source(input_source_type)

    def approximate_points(self):  # FIXME - singular matrix error
        xs, ys = zip(*self.filter_points(self.points_history))
        ws = [1] * len(xs)
        ws[-1] = 1000
        fn = self.mean_square_approximation(xs, ys, ws, 5)
        xs2 = np.linspace(xs[0], xs[-1], self.APPROXIMATION_POINTS)
        return list(zip(xs2, np.vectorize(fn)(xs2)))

    def filter_points(self):  # TODO - implement for approximation
        n = len(self)
        inf = float('inf')
        min_x = inf
        max_x = -inf

        for i in range(n, -1, -1):
            if min_x == inf and min_x == inf:
                min_x = min(min_x, self.points_history.x)
                max_x = max(max_x, self.points_history.x)
            elif min_x == inf:
                ...
            elif min_x == inf:
                ...
            else:
                ...

    @staticmethod
    def create_input_source(input_source_type):
        match input_source_type:
            case InputSource.HAND:
                return HandInput()  # TODO - add a possibility to adjust parameters
            case InputSource.FINGER:
                return FingerInput()  # TODO - add a possibility to adjust parameters
            case InputSource.MOUSE:
                return MouseInput()  # TODO - add a possibility to adjust parameters

    @staticmethod
    def mean_square_approximation(xs, ys, ws, m):
        if len(xs) != len(ys):
            raise ValueError('List of x values and list of y values must have the same length')

        n = len(xs)
        G = np.zeros((m, m), float)
        B = np.zeros(m, float)

        sums = [sum(ws[i] * xs[i] ** k for i in range(n)) for k in range(2 * m + 1)]

        for j in range(m):
            for k in range(m):
                G[j, k] = sums[j + k]

            B[j] = sum(ws[i] * ys[i] * xs[i] ** j for i in range(n))

        A = np.linalg.solve(G, B)

        return lambda x: sum(A[i] * x ** i for i in range(m))
