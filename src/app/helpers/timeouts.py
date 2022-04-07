import time
import threading


class Interval:  # I don't know if it will be useful
    def __init__(self, callback, interval, *args, **kwargs):
        self.callback = callback
        self.interval = interval
        self.thread = threading.Thread(target=self.run, args=args, kwargs=kwargs)
        self.is_running = True
        self.thread.start()

    def run(self, *args, **kwargs):
        while self.is_running:
            start_time = time.time()
            self.callback(*args, **kwargs)
            end_time = time.time()
            sleep_time = self.interval - (end_time - start_time)
            if sleep_time > 0:
                time.sleep(sleep_time)

    def clear(self):
        self.is_running = False
        self.thread.join()
