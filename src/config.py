from collections import namedtuple
from src.app.enums.input_source import InputSource
import os
from src.app.items.fruits.fruit_type import FruitType


GlobalConfig = namedtuple('GlobalConfig', [
    'game',
    'blade',
    'fruits',
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
    'LIVES',
    'DIFFICULTY'
])

BladeConfig = namedtuple('BladeConfig', [
    'COLORS',
    'VISIBILITY_DURATION',
    'INPUT_SOURCE'
])

BombConfig = namedtuple('BombConfig', [
    'SPAWN_PROBABILITY'
])

PlainFruitsConfig = namedtuple('PlainFruitsConfig', [
    'IMAGE_PATHS'
])

FruitsConfig = namedtuple('FruitsConfig', [
    'PLAIN'
])


game_config = GameConfig(
    WIDTH=800,
    HEIGHT=400,
    FPS=600,
    BACKGROUND_PATH=os.path.join('assets', 'images', 'backgrounds', 'default.jpg'),
    TITLE='Fruit Ninja',
    FRUIT_FREQUENCY=70,
    BOMB_FREQUENCY=300,
    LIVES=6,
    DIFFICULTY=1
)

blade_config = BladeConfig(
    COLORS=['White'],
    VISIBILITY_DURATION=.2,
    INPUT_SOURCE=InputSource.FINGER
)

bomb_config = BombConfig(
    SPAWN_PROBABILITY=3
)

fruits_config = FruitsConfig(
    PLAIN=PlainFruitsConfig(
        IMAGE_PATHS=[
            os.path.join('assets', 'images', 'items', 'fruits', f'{name}.png')
            for name in (
                'apple',
                'orange',
                'peach'
            )
        ]
    )
)

global_config = GlobalConfig(
    game=game_config,
    blade=blade_config,
    fruits=fruits_config,
    bomb=bomb_config
)
