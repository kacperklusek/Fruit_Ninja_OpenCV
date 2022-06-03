from threading import Thread
from enum import Enum, auto
from typing import Union
import time

from src.app.utils.timeouts import Timeout
from src.config import game_config


class AnimationFillMode(Enum):
    FORWARDS = auto()
    BACKWARDS = auto()
    BOTH = auto()
    NONE = auto()


class KeyFrame:
    def __init__(self, start_percent, function):
        self.start_percent = start_percent
        self.function = function


class Animation:
    ANIMATED_PROPERTIES = (
        'position',
        'scale',
        'alpha'
    )

    def __init__(self,
                 animated_element: object,
                 keyframes: [KeyFrame],
                 duration: Union[int, float],
                 delay: Union[int, float] = 0,
                 repetitions: [int, float('inf')] = 1,
                 fps: int = game_config.FPS,
                 animation_fill_mode: AnimationFillMode = AnimationFillMode.NONE):
        self.animation_fill_mode = animation_fill_mode
        self.animated_element = animated_element
        self.repetitions = repetitions
        self.keyframes = keyframes
        self.duration = duration
        self.delay = delay

        self._thread = None
        self._timeout = None
        self._finished = False
        self._start_time = 0
        self._last_frame_time = 0
        self._current_frame_idx = 0
        self._refresh_interval = 1 / fps

        self.__properties_copy = self._copy_animated_properties()
        self._apply_fill_mode()

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
    def started(self):
        return self._start_time > 0

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
        self._thread = Thread(target=self.run)
        self._timeout = Timeout(self._start_after_delay, self.delay)

    def finish(self):
        self._finished = True
        self._apply_fill_mode()

    def reset(self):
        self._start_time = time.time()
        self._last_frame_time = self._start_time
        self._current_frame_idx = 0

    def run(self):
        i = 0
        while i < self.repetitions and not self._finished:
            self.reset()
            self._run_animation_frames(i)
            i += 1

    def _apply_fill_mode(self):
        if self.finished:
            # Reset element properties after animation
            if self.animation_fill_mode in {AnimationFillMode.NONE, AnimationFillMode.BACKWARDS}:
                self._restore_animated_properties()
        elif not self.started:
            # Apply initial animations
            if self.keyframes and self.keyframes[0].function:
                self.keyframes[0].function(self.animated_element, 0)

    def _copy_animated_properties(self):
        copy = {}
        for prop in self.ANIMATED_PROPERTIES:
            if prop in dir(self.animated_element):
                copy[prop] = getattr(self.animated_element, prop)
        return copy

    def _restore_animated_properties(self):
        for prop, value in self.__properties_copy.items():
            setattr(self.animated_element, prop, value)

    def _start_after_delay(self):
        self._start_time = time.time()
        self._last_frame_time = self._start_time
        self._thread.start()

    def _run_animation_frames(self, current_repetition):
        while self.next_keyframe:
            curr_time = time.time()
            percent = (curr_time - self._start_time) / self.duration

            if percent >= 1:
                if current_repetition == self.repetitions:
                    self.finish()
                return

            frame_duration_percent = self.next_keyframe.start_percent - self.current_keyframe.start_percent
            current_frame_percent = (percent - self.current_keyframe.start_percent) / frame_duration_percent
            current_frame_function = self.current_keyframe.function

            if current_frame_function:
                current_frame_function(self.animated_element, current_frame_percent)

            if percent >= self.next_keyframe.start_percent:
                self._current_frame_idx += 1

            time.sleep(self._refresh_interval)


def scale_animation(from_scale, to_scale, animation_timing_function=lambda x: x):
    def apply(element, percent):
        percent = animation_timing_function(percent)
        element.scale = abs(to_scale - from_scale) * (percent if to_scale > from_scale else 1 - percent)
    return apply


def alpha_animation(from_alpha, to_alpha, animation_timing_function=lambda x: x):
    def apply(element, percent):
        percent = animation_timing_function(percent)
        if from_alpha < to_alpha:
            element.alpha = from_alpha + percent * (to_alpha - from_alpha)
        else:
            element.alpha = from_alpha - percent * (from_alpha - to_alpha)
    return apply


def position_animation(from_vector, to_vector, animation_timing_function=lambda x: x):
    def apply(element, percent):
        percent = animation_timing_function(percent)
        delta_vector = to_vector - from_vector
        element.position = from_vector + percent * delta_vector
    return apply


def fade_animation(from_scale, to_scale, from_alpha, to_alpha, animation_timing_function=lambda x: x):
    def apply(element, percent):
        scale_animation(from_scale, to_scale, animation_timing_function)(element, percent)
        alpha_animation(from_alpha, to_alpha, animation_timing_function)(element, percent)
    return apply


def cubic_timing(percent):
    return percent ** 3
