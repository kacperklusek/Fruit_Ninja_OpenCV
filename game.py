import pygame
from collections import deque
from pygame.math import Vector2

FPS = 60

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Fruit Ninja')
clock = pygame.time.Clock()
game_active = True

coords = deque()
max_count = 10

test_surface = pygame.Surface((800, 400))

while True:
    test_surface.fill('Black')
    if coords: coords.popleft()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEMOTION:
                coords.append(event.pos)
                if len(coords) > max_count:
                    coords.popleft()


    if len(coords) > 1: pygame.draw.lines(test_surface, 'Red', False, coords, 4)

    screen.blit(test_surface, (0, 0))
    pygame.display.update()
    clock.tick(FPS)

