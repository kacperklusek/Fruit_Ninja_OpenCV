import pygame
import time
from .input_source import InputSource


class MouseInput(InputSource):
    def __init__(self,
                 visibility_duration=.05,
                 refresh_frequency=144):
        InputSource.__init__(self, visibility_duration)
        self.refresh_frequency = refresh_frequency
        self.interval = 1 / refresh_frequency
        self.is_tracking = False

    def start_tracking(self):
        self.is_tracking = True
        super().start_tracking()

    def end_tracking(self):
        self.is_tracking = False
        super().end_tracking()

    def run(self, callback):
        while self.is_tracking:
            start_time = time.time()

            # Save mouse position only if mouse cursor is inside the game window
            if pygame.mouse.get_focused():
                self.add_to_history(pygame.mouse.get_pos())
            callback()

            end_time = time.time()
            sleep_time = self.interval - (end_time - start_time)
            if sleep_time > 0:
                time.sleep(sleep_time)
