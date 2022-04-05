from cv2 import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=3)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        hand = hands[0] if len(hands) == 1 or hands[0]['type'] == 'Right' else hands[1]
        point = hand['lmList'][8]
        print(point)

    cv2.imshow('Image', img)
    cv2.waitKey(1)
