import time
from threading import Thread, Lock

from src.app.controllers.time_controller import TimeController


class Interval:
    def __init__(self, callback, interval, mutex=None, *args, **kwargs):
        self.callback = callback
        self.interval = interval
        self.mutex = mutex or Lock()
        self.time_controller = TimeController()
        self.thread = Thread(target=self.run, args=args, kwargs=kwargs)
        self.is_running = True
        self.thread.start()

    def run(self, *args, **kwargs):
        while self.is_running:
            start_time = time.time()
            self.mutex.acquire(True)
            self.callback(*args, **kwargs)
            self.mutex.release()
            end_time = time.time()
            sleep_time = self.interval / self.time_controller.ratio - (end_time - start_time)
            if sleep_time > 0:
                time.sleep(sleep_time)

    def clear(self):
        self.is_running = False
        self.thread.join()
