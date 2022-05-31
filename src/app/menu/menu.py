from abc import ABC, abstractmethod
from src.app.menu.buttons import NewGameButton, DojoButton, QuitButton
from src.config import window_config
from pygame.math import Vector2


class Menu(ABC):  # TODO
    def __init__(self, game):
        self.game = game

    @abstractmethod
    def display(self):
        pass


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.new_game_button = NewGameButton(Vector2(window_config.WIDTH / 4, window_config.HEIGHT * 3 / 4))
        self.dojo_button = DojoButton(Vector2(window_config.WIDTH / 2, window_config.HEIGHT * 3 / 4))
        self.quit_button = QuitButton(Vector2(window_config.WIDTH * 3 / 4, window_config.HEIGHT * 3 / 4))

    # TODO - maybe implement own @override decorator
    def display(self):
        self.new_game_button.update(self.game.screen)
        self.dojo_button.update(self.game.screen)
        self.quit_button.update(self.game.screen)

        if self.game.blade.collides(self.new_game_button):
            self.game.game_started = True

        if self.game.blade.collides(self.dojo_button):
            print('dojo', self.new_game_button.rect)

        if self.game.blade.collides(self.quit_button):
            print('quit game', self.new_game_button.rect)
