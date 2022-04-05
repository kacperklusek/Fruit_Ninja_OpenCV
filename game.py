import pygame
from collections import deque
from pygame.math import Vector2

from cv2 import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=3)


FPS = 200

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Fruit Ninja')
clock = pygame.time.Clock()
game_active = True

coords = deque()
max_count = 10

test_surface = pygame.Surface((800, 400))


while True:
    # hand detection shit in here
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)
    # hand detection done

    test_surface.fill('Black')
    # if coords: coords.popleft()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if game_active:
        if hands:
            hand = hands[0] if len(hands) == 1 or hands[0]['type'] == 'Right' else hands[1]
            fingerpos = hand['lmList'][8]
            coords.append(fingerpos[:2])
        if len(coords) > max_count:
            coords.popleft()

    if len(coords) > 1: pygame.draw.lines(test_surface, 'Red', False, coords, 4)

    screen.blit(test_surface, (0, 0))
    pygame.display.update()
    clock.tick(FPS)
