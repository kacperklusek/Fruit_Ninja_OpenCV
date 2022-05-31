from abc import ABC, abstractmethod
from src.config import game_config
import pygame


class Menu(ABC):  # TODO
    def __init__(self, blade):
        self.blade = blade
        self.is_displayed = False

    @abstractmethod
    def display(self):
        pass


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    # TODO - maybe implement own @override decorator
    def display(self):
        while self.is_displayed:
            ...
