import pygame
from pygame.math import Vector2
from collections import deque

from cv2 import cv2
import mediapipe as mp

from src.app.items.fruits.fruit import Fruit, FruitType

mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

WIDTH = 800
HEIGHT = 400
FPS = 200

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Fruit Ninja')
clock = pygame.time.Clock()
game_active = True

coords = deque()
max_count = 5

test_surface = pygame.Surface((WIDTH, HEIGHT))

Fruit(FruitType.Apple, Vector2(400, 200), Vector2(-5, -20))


def get_cv_results():
    success, image = cap.read()
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return hands.process(image)


def get_coords():
    normalized_landmark = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    return [WIDTH - normalized_landmark.x * WIDTH, normalized_landmark.y * HEIGHT]


line = pygame.sprite.Sprite()

with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    while True:
        test_surface.fill('Black')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if game_active:
            if cap.isOpened():
                results = get_cv_results()
                if results and results.multi_hand_landmarks:
                    pixel_coords = get_coords()
                    coords.append(pixel_coords)
                if len(coords) > max_count:
                    coords.popleft()

        if len(coords) > 1: pygame.draw.lines(test_surface, 'White', False, coords, 4)

        # check collision and remove colliding
        if coords and pixel_coords:
            for fruit in Fruit.group:
                if fruit.rect.collidepoint(coords[-1]):
                    fruit.kill()

        Fruit.group.update()
        Fruit.group.draw(test_surface)
        screen.blit(test_surface, (0, 0))
        pygame.display.update()
        clock.tick(FPS)
