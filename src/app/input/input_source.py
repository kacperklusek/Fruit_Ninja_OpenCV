from collections import deque
import threading
from abc import ABC, abstractmethod


class InputSource(ABC):
    def __init__(self, history_size=10):
        self.points_history = deque()
        self.history_size = history_size
        self.thread = None

    def start_tracking(self):
        if self.thread: return
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def end_tracking(self):
        self.thread.join()

    def update_history(self, point):
        self.points_history.append(point)
        if len(self.points_history) > self.history_size:
            self.points_history.popleft()

    @abstractmethod
    def run(self):
        pass
