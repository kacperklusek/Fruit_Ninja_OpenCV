import threading
import time
from abc import ABC, abstractmethod


class MenuElement(ABC):
    @abstractmethod
    def blit(self, surface):
        pass


class AnimatedMenuElement(MenuElement):
    @abstractmethod
    def animate(self):
        pass


class KeyFrame:
    def __init__(self, start_percent, function):
        self.start_percent = start_percent
        self.function = function


class Animation:
    def __init__(self, animated_element, duration, keyframes=[], fps: int = 144):
        self.animated_element = animated_element
        self.duration = duration

        self._keyframes: [KeyFrame] = keyframes
        self._start_time = 0
        self._current_frame_idx = 0
        self._thread = None
        self._last_frame_time = 0
        self._refresh_interval = 1 / fps
        self._finished = False

    def __len__(self):
        return len(self.keyframes)

    def __getitem__(self, idx):
        return self.keyframes[idx]

    @property
    def current_keyframe(self):
        return self.keyframes[self._current_frame_idx]

    @property
    def next_keyframe(self):
        if self._current_frame_idx == len(self) - 1:
            return self.current_keyframe
        return self.keyframes[self._current_frame_idx + 1]

    @property
    def keyframes(self):
        return self._keyframes

    @property
    def finished(self):
        return self._finished

    @keyframes.setter
    def keyframes(self, keyframes_list):
        self._keyframes = keyframes_list

    def add(self, keyframe):
        self.keyframes.append(keyframe)

    def start(self):
        self.keyframes.append(KeyFrame(1, None))
        self._thread = threading.Thread(target=self.run)
        self._start_time = time.time()
        self._last_frame_time = self._start_time
        self._thread.start()

    def run(self):
        while self.next_keyframe:
            curr_time = time.time()
            percent = (curr_time - self._start_time) / self.duration
            if percent >= 1:
                self._finished = True
                return

            frame_duration_percent = self.next_keyframe.start_percent - self.current_keyframe.start_percent
            current_frame_percent = (percent - self.current_keyframe.start_percent) / frame_duration_percent
            current_frame_function = self.current_keyframe.function

            if current_frame_function:
                current_frame_function(self.animated_element, current_frame_percent)

            if percent >= self.next_keyframe.start_percent:
                self._current_frame_idx += 1

            time.sleep(self._refresh_interval)
