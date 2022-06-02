import time

from src.app.gui.labels import ComboLabel
from src.app.items.fruit import Fruit


class ScoreController:
    COMBO_TIME_DIFF = .2
    MIN_FRUITS_COUNT = 3

    def __init__(self):
        self.last_fruit_kill_time = 0
        self.combo = 0
        self._score = 0
        self.observers = []
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

    def check_combo_finished(self, surface):
        curr_time = time.time()
        if curr_time - self.last_fruit_kill_time > self.COMBO_TIME_DIFF:
            if self.combo >= self.MIN_FRUITS_COUNT:
                self.display_combo(surface)
                self.score += self.combo
            self.combo = 0

    def display_combo(self, surface):
        label = ComboLabel(self.combo, self.last_fruit_kill_position)
        label.blit(surface)
