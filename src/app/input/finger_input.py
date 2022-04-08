from .camera_input import CameraInput


class FingerInput(CameraInput):
    def __init__(self, visibility_duration=.25, finger_code=CameraInput.mp_hands.HandLandmark.INDEX_FINGER_TIP):
        CameraInput.__init__(self, visibility_duration)
        self.finger_code = finger_code

    def get_coords(self, results):
        coords = results.multi_hand_landmarks[0].landmark[self.finger_code]
        return [(1 - coords.x) * 800, coords.y * 600]
