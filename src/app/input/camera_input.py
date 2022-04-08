from cv2 import cv2
import mediapipe as mp
from .input_source import InputSource
from abc import ABC, abstractmethod

mp_drawing = mp.solutions.drawing_utils


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
