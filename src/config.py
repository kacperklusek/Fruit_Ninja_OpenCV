from collections import namedtuple
from src.app.enums.input_source import InputSource
import os
from src.app.items.fruits.fruit_type import FruitType

GlobalConfig = namedtuple('GlobalConfig', [
    'game',
    'blade',
    'fruit',
    'bomb'
])

GameConfig = namedtuple('GameConfig', [
    'TITLE',
    'WIDTH',
    'HEIGHT',
    'FPS',
    'BACKGROUND_PATH',
    'FRUIT_FREQUENCY',
    'BOMB_FREQUENCY',
    'LIFES',
    'DIFFICULTY'
])

BladeConfig = namedtuple('BladeConfig', [
    'COLORS',
    'VISIBILITY_DURATION',
    'INPUT_SOURCE'
])

FruitConfig = namedtuple('FruitConfig', [
    'SPAWN_PROBABILITY',
    'IMAGE_PATH',
    'FRUIT_TYPE',
    'FALLING_TIME'
])

BombConfig = namedtuple('BombConfig', [
    'SPAWN_PROBABILITY',
    'FALLING_TIME'
])


game_config = GameConfig(
    WIDTH=800,
    HEIGHT=400,
    FPS=60,
    BACKGROUND_PATH=os.path.join('assets', 'images', 'backgrounds', 'default.jpg'),
    TITLE='Fruit Ninja',
    FRUIT_FREQUENCY=70,
    BOMB_FREQUENCY=300,
    LIFES=3,
    DIFFICULTY=1
)

blade_config = BladeConfig(
    COLORS=['White'],
    VISIBILITY_DURATION=.2,
    INPUT_SOURCE=InputSource.FINGER
)

fruit_config = FruitConfig(
    SPAWN_PROBABILITY=10,
    IMAGE_PATH=os.path.join('assets', 'images', 'items', 'fruits', 'apple.png'),
    FRUIT_TYPE=FruitType.APPLE,
    FALLING_TIME=2
)

bomb_config = BombConfig(
    SPAWN_PROBABILITY=3,
    FALLING_TIME=2
)

global_config = GlobalConfig(
    game=game_config,
    blade=blade_config,
    fruit=fruit_config,
    bomb=bomb_config
)

APPLE_IMG_PATH = os.path.join('assets', 'images', 'items', 'fruits', 'apple.png')
ORANGE_IMG_PATH = os.path.join('assets', 'images', 'items', 'fruits', 'orange.png')
PEACH_IMG_PATH = os.path.join('assets', 'images', 'items', 'fruits', 'peach.png')
