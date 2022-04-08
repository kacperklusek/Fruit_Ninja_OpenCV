import pygame
from pygame.math import Vector2

from src.app.items.fruits.fruit import Fruit, FruitType
from src.app.input.finger_input import FingerInput
from src.app.input.mouse_input import MouseInput
from src.app.input.hand_input import HandInput

WIDTH = 800
HEIGHT = 400
FPS = 200

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Fruit Ninja')
clock = pygame.time.Clock()
game_active = True


test_surface = pygame.Surface((WIDTH, HEIGHT))

Fruit(FruitType.Apple, Vector2(400, 200), Vector2(-5, -20))

input_source = HandInput()
# input_source = FingerInput()
# input_source = MouseInput()
input_source.start_tracking()


while True:
    test_surface.fill('Black')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            input_source.end_tracking()
            pygame.quit()
            exit()

    if len(input_source.points_history) > 1:
        pygame.draw.lines(test_surface, 'White', False, input_source.points_history, 4)

    # check collision and remove colliding
    if input_source.points_history:
        for fruit in Fruit.group:
            if fruit.rect.collidepoint(input_source.points_history[-1]):
                fruit.kill()

    Fruit.group.update()
    Fruit.group.draw(test_surface)
    screen.blit(test_surface, (0, 0))
    pygame.display.update()
    clock.tick(FPS)
