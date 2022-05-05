from time import time


class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if isinstance(cls._instance, cls):
            raise Exception('ERROR!!!!!!')  #TODO
        cls._instance = object.__new__(cls)
        return cls._instance


class TimeController(Singleton):
    MAX_RATIO = 100
    _last_frame_time = 0
    _last_spawn_time = 0
    _last_frame_duration = 0
    _init_time = 0
    _ratio = 1

    # @property
    # def ratio(cls):
    #     return cls._ratio
    #
    # @ratio.setter
    # def ratio(cls, ratio):
    #     if not 0 < ratio <= cls.MAX_RATIO:
    #         raise ValueError(f'ratio should be between 0 and {cls.MAX_RATIO}')
    #     cls._ratio = ratio

    @classmethod
    def set_ratio(cls, ratio):
        if not 0 < ratio <= cls.MAX_RATIO:
            raise ValueError(f'ratio should be between 0 and {cls.MAX_RATIO}')
        cls._ratio = ratio

    @classmethod
    def init_game_timing(cls):
        cls._init_time = time()

    @classmethod
    @property
    def total_elapsed_time(cls) -> float:
        return time() - cls._init_time

    @classmethod
    def update_last_frame_time(cls):
        curr_time = time()
        if cls._last_frame_time:
            cls._last_frame_duration = curr_time - cls._last_frame_time
        cls._last_frame_time = curr_time

    @classmethod
    def update_last_spawn_time(cls):
        cls._last_spawn_time = time()

    @classmethod
    @property
    def get_last_frame_duration(cls) -> float:
        return cls._last_frame_duration * cls._ratio

    @classmethod
    @property
    def get_interval_since_last_spawn(cls) -> float:
        return time() - cls._last_spawn_time
