import time
from pygame.sprite import Group
from pygame.font import Font

from src.app.gui.labels import AnimatedLabel
from src.app.items.fruit import Fruit
from src.config import effects_config, game_config


class ScoreController:
    def __init__(self, combo_group: Group):
        self.combo_group = combo_group
        self._combo = 0
        self._score = 0
        self._observers = []
        self._last_fruit_kill_time = 0
        self._last_fruit_kill_position = None

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score):
        self._score = score
        self.notify_score_changed()

    def reset(self):
        self._last_fruit_kill_time = 0
        self._combo = 0
        self._score = 0

    def add_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def notify_score_changed(self):
        for observer in self._observers:
            observer.update_score(self.score)

    def register_fruit_cut(self, fruit: Fruit):
        self.score += 1

        curr_time = time.time()
        if curr_time - self._last_fruit_kill_time <= game_config.COMBO_TIME_DIFF:
            self._combo += 1 if self._combo > 0 else 2

        self._last_fruit_kill_time = curr_time
        self._last_fruit_kill_position = fruit.position

    def check_combo_finished(self):
        curr_time = time.time()
        if curr_time - self._last_fruit_kill_time > game_config.COMBO_TIME_DIFF:
            if self._combo >= game_config.MIN_COMBO_FRUITS:
                self.display_combo()
                self.score += self._combo
            self._combo = 0

    def display_combo(self):
        font = game_config.FONT
        size = effects_config.COMBO_FONT_SIZE
        color = effects_config.COMBO_TEXT_COLOR

        AnimatedLabel([
                Font(font, int(size * .8)).render(f'{self._combo} fruits', True, color),
                Font(font, size).render('combo', True, color),
            ],
            self._last_fruit_kill_position,
            effects_config.COMBO_DISPLAY_DURATION,
            self.combo_group
        )
