from .camera_input import CameraInput
from functools import reduce


class HandInput(CameraInput):
    def __init__(self, visibility_duration=.25):
        CameraInput.__init__(self, visibility_duration)

    def get_coords(self, results):
        landmarks = results.multi_hand_landmarks[0].landmark
        x, y = reduce(lambda acc, p: (acc[0] + p.x, acc[1] + p.y), landmarks, (0, 0))
        return [(1 - x / 21) * 800, y / 21 * 600]
