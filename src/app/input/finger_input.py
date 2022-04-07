from cv2 import cv2
import mediapipe as mp
from .input_source import InputSource


class FingerInput(InputSource):
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    def __init__(self,
                 history_size=10,
                 finger_code=mp_hands.HandLandmark.INDEX_FINGER_TIP):
        InputSource.__init__(self)
        self.history_size = history_size
        self.finger_code = finger_code
        self.camera = None

    def start_tracking(self):
        self.camera = cv2.VideoCapture(0)
        super().start_tracking()

    def end_tracking(self):
        self.camera.release()
        super().end_tracking()

    def get_cv_results(self, hands):
        ret, image = self.camera.read()
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return hands.process(image)

    def run(self):
        with self.mp_hands.Hands(
                model_complexity=0,
                min_detection_confidence=0.75,
                min_tracking_confidence=0.5) as hands:

            while self.camera.isOpened():
                results = self.get_cv_results(hands)

                if results and results.multi_hand_landmarks:
                    self.update_history(self.get_coords(results))

                cv2.waitKey(1)

    def get_coords(self, results):
        normalized_landmark = results.multi_hand_landmarks[0].landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        return [800 - normalized_landmark.x * 800, normalized_landmark.y * 600]
