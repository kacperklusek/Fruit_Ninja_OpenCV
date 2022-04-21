import time
import pygame
import threading
import mediapipe as mp
from cv2 import cv2
from functools import reduce
from collections import deque
from src.config import game_config
from abc import ABC, abstractmethod
from src.app.helpers.point import Point


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
        self._points_history.append(InputPoint(Point(*coords), time.time()))

    def update_blade(self):
        while self._points_history and time.time() - self._points_history[0].time_added >= self.visibility_duration:
            self._points_history.popleft()

    @abstractmethod
    def run(self, callback):
        pass


class CameraInput(InputSource, ABC):
    mp_hands = mp.solutions.hands

    def __init__(self, visibility_duration):
        InputSource.__init__(self, visibility_duration)
        self.camera = None

    def start_tracking(self):
        self.camera = cv2.VideoCapture(0)
        super().start_tracking()

    def end_tracking(self):
        self.camera.release()
        super().end_tracking()

    def get_cv_results(self, hands):
        ret, image = self.camera.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        return results

    def run(self, callback):
        with self.mp_hands.Hands(
                model_complexity=0,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as hands:

            while self.camera.isOpened():
                results = self.get_cv_results(hands)

                if results and results.multi_hand_landmarks:
                    self.add_to_history(self.get_coords(results))

                callback()
                cv2.waitKey(1)

    @abstractmethod
    def get_coords(self, results):
        pass


class FingerInput(CameraInput):
    def __init__(self, visibility_duration=.25, finger_code=CameraInput.mp_hands.HandLandmark.INDEX_FINGER_TIP):
        CameraInput.__init__(self, visibility_duration)
        self.finger_code = finger_code

    def get_coords(self, results):
        coords = results.multi_hand_landmarks[0].landmark[self.finger_code]
        return (1 - coords.x) * game_config.WIDTH, coords.y * game_config.HEIGHT


class HandInput(CameraInput):
    def __init__(self, visibility_duration=.25):
        CameraInput.__init__(self, visibility_duration)

    def get_coords(self, results):
        landmarks = results.multi_hand_landmarks[0].landmark
        x, y = reduce(lambda acc, p: (acc[0] + p.x, acc[1] + p.y), landmarks, (0, 0))
        n = len(landmarks)
        return (1 - x / n) * game_config.WIDTH, y / n * game_config.HEIGHT


class MouseInput(InputSource):
    def __init__(self, visibility_duration=.05, refresh_frequency=144):
        InputSource.__init__(self, visibility_duration)
        self.refresh_frequency = refresh_frequency
        self.interval = 1 / refresh_frequency
        self.is_tracking = False

    def start_tracking(self):
        self.is_tracking = True
        super().start_tracking()

    def end_tracking(self):
        self.is_tracking = False
        super().end_tracking()

    def run(self, callback):
        while self.is_tracking:
            start_time = time.time()

            # Save mouse position only if mouse cursor is inside the game window
            if pygame.mouse.get_focused():
                self.add_to_history(pygame.mouse.get_pos())
            callback()

            end_time = time.time()
            sleep_time = self.interval - (end_time - start_time)
            if sleep_time > 0:
                time.sleep(sleep_time)
