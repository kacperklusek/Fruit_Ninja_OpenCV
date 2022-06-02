import time


class ScoreController:
    COMBO_TIME_DIFF = .2
    MIN_FRUITS_COUNT = 3

    def __init__(self):
        self.last_fruit_kill_time = 0
        self.combo = 0
        self._score = 0

    @property
    def score(self):
        return self._score

    def reset(self):
        self.last_fruit_kill_time = 0
        self.combo = 0
        self._score = 0

    def register_fruit_cut(self):
        self._score += 1

        curr_time = time.time()
        if curr_time - self.last_fruit_kill_time <= self.COMBO_TIME_DIFF:
            self.combo += 1 if self.combo > 0 else 2
            print(self.combo)

        self.last_fruit_kill_time = curr_time

    def check_combo_finished(self):
        curr_time = time.time()
        if curr_time - self.last_fruit_kill_time > self.COMBO_TIME_DIFF and self.combo >= self.MIN_FRUITS_COUNT:
            self.display_combo()
            self._score += self.combo
            self.combo = 0

    def display_combo(self):
        print(f'COMBO {self.combo}')
