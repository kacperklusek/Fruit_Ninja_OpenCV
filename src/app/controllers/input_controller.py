import time
import pygame
import mediapipe as mp
from threading import Lock, Thread
from cv2 import cv2
from functools import reduce
from collections import deque
from abc import ABC, abstractmethod
from src.app.utils.point import Point
from src.config import mouse_input_config, \
    hand_input_config, finger_input_config, \
    window_config, blade_config


class InputPoint:
    def __init__(self, coords, time_added):
        self.coords = coords
        self.time_added = time_added


class InputController(ABC):
    def __init__(self):
        self.thread = None
        self._mutex = Lock()
        self._points_history = deque()

    @property
    def points_history(self):
        self._mutex.acquire(True)
        history = list(map(lambda point: point.coords, self._points_history))
        self._mutex.release()
        return history

    def start_tracking(self):
        if self.thread: return
        self.thread = Thread(target=self.run, args=(self.update_blade,))
        self.thread.start()

    def end_tracking(self):
        self.thread.join()

    def add_to_history(self, coords):
        self._mutex.acquire(True)
        self._points_history.append(InputPoint(Point(*coords), time.time()))
        self._mutex.release()

    def clear_history(self):
        self._mutex.acquire(True)
        self._points_history.clear()
        self._mutex.release()

    def update_blade(self):
        self._mutex.acquire(True)
        while self._points_history and \
                time.time() - self._points_history[0].time_added >= blade_config.VISIBILITY_DURATION:
            self._points_history.popleft()
        self._mutex.release()

    @abstractmethod
    def get_points_for_collision(self):
        pass

    @abstractmethod
    def run(self, callback):
        pass


class CameraInput(InputController, ABC):
    mp_hands = mp.solutions.hands

    def __init__(self, min_detection_confidence, min_tracking_confidence):
        InputController.__init__(self)
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
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
                min_detection_confidence=self.min_detection_confidence,
                min_tracking_confidence=self.min_tracking_confidence) as hands:

            while self.camera.isOpened():
                results = self.get_cv_results(hands)

                if results and results.multi_hand_landmarks:
                    self.add_to_history(self.get_coords(results))

                callback()
                cv2.waitKey(1)

    @abstractmethod
    def get_coords(self, results):
        pass

    def get_points_for_collision(self):
        current_time = time.time()
        if len(self._points_history) >= 5:
            points = self._points_history[-5:]
        else:
            points = self._points_history[:]

        while current_time - points[0].time_added > blade_config.VALIDITY_DURATION_FOR_COLLISION:
            points.popleft()

        return points


class FingerInput(CameraInput):
    def __init__(self):
        CameraInput.__init__(
            self,
            finger_input_config.MIN_DETECTION_CONFIDENCE,
            finger_input_config.MIN_TRACKING_CONFIDENCE
        )
        self.finger_code = finger_input_config.FINGER_CODE

    def get_coords(self, results):
        coords = results.multi_hand_landmarks[-1].landmark[self.finger_code]
        return (1 - coords.x) * window_config.WIDTH, coords.y * window_config.HEIGHT


class HandInput(CameraInput):
    def __init__(self):
        CameraInput.__init__(
            self,
            hand_input_config.MIN_DETECTION_CONFIDENCE,
            hand_input_config.MIN_TRACKING_CONFIDENCE
        )

    def get_coords(self, results):
        landmarks = results.multi_hand_landmarks[0].landmark
        x, y = reduce(lambda acc, p: (acc[0] + p.x, acc[1] + p.y), landmarks, (0, 0))
        n = len(landmarks)
        return (1 - x / n) * window_config.WIDTH, y / n * window_config.HEIGHT


class MouseInput(InputController):
    def __init__(self):
        InputController.__init__(self)
        self.interval = 1 / mouse_input_config.REFRESH_FREQUENCY
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
            if pygame.mouse.get_focused() and pygame.mouse.get_pressed()[0]:
                pygame.mouse.set_visible(False)
                self.add_to_history(pygame.mouse.get_pos())
            else:
                pygame.mouse.set_visible(True)
            callback()

            end_time = time.time()
            sleep_time = self.interval - (end_time - start_time)
            if sleep_time > 0:
                time.sleep(sleep_time)

    def get_points_for_collision(self):
        current_time = time.time()
        if len(self.points_history) == 0 or \
                current_time - self._points_history[-1].time_added > blade_config.VALIDITY_DURATION_FOR_COLLISION:
            return []
        else:
            return [self.points_history[-1]]
