import time
from pygame.sprite import Group
from pygame.font import Font

from src.app.gui.labels import AnimatedLabel
from src.app.items.fruit import Fruit
from src.config import effects_config, game_config


class ScoreController:
    COMBO_TIME_DIFF = .2
    MIN_FRUITS_COUNT = 3

    def __init__(self, combo_group: Group):
        self.combo = 0
        self._score = 0
        self.observers = []
        self.combo_group = combo_group
        self.last_fruit_kill_time = 0
        self.last_fruit_kill_position = None

    def add_observer(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def notify_score_changed(self):
        for observer in self.observers:
            observer.update_score(self.score)

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score):
        self._score = score
        self.notify_score_changed()

    def reset(self):
        self.last_fruit_kill_time = 0
        self.combo = 0
        self.score = 0

    def register_fruit_cut(self, fruit: Fruit):
        self.score += 1

        curr_time = time.time()
        if curr_time - self.last_fruit_kill_time <= self.COMBO_TIME_DIFF:
            self.combo += 1 if self.combo > 0 else 2

        self.last_fruit_kill_time = curr_time
        self.last_fruit_kill_position = fruit.position

    def check_combo_finished(self):
        curr_time = time.time()
        if curr_time - self.last_fruit_kill_time > self.COMBO_TIME_DIFF:
            if self.combo >= self.MIN_FRUITS_COUNT:
                self.display_combo()
                self.score += self.combo
            self.combo = 0

    def display_combo(self):
        font = game_config.FONT
        size = effects_config.COMBO_FONT_SIZE
        color = effects_config.COMBO_TEXT_COLOR

        AnimatedLabel([
                Font(font, int(size * .8)).render(f'{self.combo} fruits', True, color),
                Font(font, size).render('combo', True, color),
            ],
            self.last_fruit_kill_position,
            effects_config.COMBO_DISPLAY_DURATION,
            self.combo_group
        )
