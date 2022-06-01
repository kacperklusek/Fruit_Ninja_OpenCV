import pygame.mixer
from pygame import mixer

from src.config import sound_config

pygame.mixer.init()


class SoundController:  # TODO
    _throw_sound = mixer.Sound(sound_config.THROW)
    _throw_sound.set_volume(sound_config.THROW_VOLUME)

    _boom_sound = mixer.Sound(sound_config.BOOM)
    _boom_sound.set_volume(sound_config.BOOM_VOLUME)

    _game_over_sound = mixer.Sound(sound_config.OVER)
    _game_over_sound.set_volume(sound_config.OVER_VOLUME)

    _game_start_sound = mixer.Sound(sound_config.START)
    _game_start_sound.set_volume(sound_config.START_VOLUME)

    _splatter_sound = mixer.Sound(sound_config.SPLATTER)
    _splatter_sound.set_volume(sound_config.SPLATTER_VOLUME)

    _menu_sound = mixer.Sound(sound_config.MENU)
    _menu_sound.set_volume(sound_config.MENU_VOLUME)

    def __init__(self):
        ...

    @classmethod
    def play_throw_sound(cls):
        cls._throw_sound.play()

    @classmethod
    def play_boom_sound(cls):
        cls._boom_sound.play()

    @classmethod
    def play_game_over_sound(cls):
        print('over')
        cls._game_over_sound.play()

    @classmethod
    def play_game_start_sound(cls):
        cls._game_start_sound.play()

    @classmethod
    def play_splatter_sound(cls):
        cls._splatter_sound.play()

    @classmethod
    def play_menu_sound(cls):
        cls._menu_sound.play(-1)

    @classmethod
    def stop_menu_sound(cls):
        cls._menu_sound.stop()
