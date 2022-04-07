import time
import threading
from collections import deque
from abc import ABC, abstractmethod


class InputPoint:
    def __init__(self, coords, time_added):
        self.coords = coords
        self.time_added = time_added


class InputSource(ABC):
    def __init__(self, visibility_duration):
        self.visibility_duration = visibility_duration
        self.thread = None
        self._points_history = deque()

    @property
    def points_history(self):
        return list(map(lambda point: point.coords, self._points_history))

    def start_tracking(self):
        if self.thread: return
        self.thread = threading.Thread(target=self.run, args=(self.update_blade,))
        self.thread.start()

    def end_tracking(self):
        self.thread.join()

    def add_to_history(self, coords):
        self._points_history.append(InputPoint(coords, time.time()))

    def update_blade(self):
        while self._points_history and time.time() - self._points_history[0].time_added >= self.visibility_duration:
            self._points_history.popleft()

    @abstractmethod
    def run(self, callback):
        pass
