from time import time
from src.app.utils.design_patterns import Singleton


class TimeController(Singleton):
    MIN_RATIO = .25
    MAX_RATIO = 10

    def __init__(self):
        self.__ratio = 1
        self.__start_time = 0
        self.__last_frame_time = 0
        self.__last_frame_duration = 0

    def init(self):
        self.__start_time = self.__last_frame_time = time()

    @property
    def ratio(self):
        return self.__ratio

    @ratio.setter
    def ratio(self, ratio):
        if ratio <= 0:
            raise ValueError(f'Time ratio should be greater than {self.MIN_RATIO}')
        if ratio > self.MAX_RATIO:
            raise ValueError(f'Time ratio shouldn\'t be greater than {self.MAX_RATIO}')
        self.__ratio = ratio

    @property
    def last_frame_time(self):
        return self.__last_frame_time

    @property
    def last_frame_duration(self):
        return self.__last_frame_duration * self.ratio

    @property
    def total_elapsed_time(self):
        return (time() - self.__start_time) * self.ratio

    def register_new_frame(self):
        curr_time = time()
        self.__last_frame_duration = curr_time - self.__last_frame_time
        self.__last_frame_time = curr_time
