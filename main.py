from cv2 import cv2
from cvzone.HandTrackingModule import HandDetector

import cv2
import mediapipe

drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands

capture = cv2.VideoCapture(0)

frameWidth = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
frameHeight = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

circleCenter = (round(frameWidth / 2), round(frameHeight / 2))
circleRadius = 40

with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7,
                       max_num_hands=1) as hands:
    while (True):

        ret, frame = capture.read()

        if ret == False:
            continue

        frame = cv2.flip(frame, 1)

        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        circleColor = (0, 0, 0)

        if results.multi_hand_landmarks != None:

            normalizedLandmark = results.multi_hand_landmarks[0].landmark[handsModule.HandLandmark.INDEX_FINGER_TIP]
            pixelCoordinatesLandmark = drawingModule._normalized_to_pixel_coordinates(normalizedLandmark.x,
                                                                                      normalizedLandmark.y,
                                                                                      frameWidth,
                                                                                      frameHeight)

            cv2.circle(frame, pixelCoordinatesLandmark, 2, (255, 0, 0), -1)


        cv2.circle(frame, circleCenter, circleRadius, circleColor, -1)

        cv2.imshow('Test image', frame)

        if cv2.waitKey(1) == 27:
            break

cv2.destroyAllWindows()
capture.release()