from collections import namedtuple
from src.app.enums.input_source import InputSource


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
    'BACKGROUND_COLOR',
    'FRUIT_FREQUENCY',
    'BOMB_FREQUENCY'
])

BladeConfig = namedtuple('BladeConfig', [
    'COLORS',
    'VISIBILITY_DURATION',
    'INPUT_SOURCE'
])

FruitConfig = namedtuple('FruitConfig', [
    'SPAWN_INTERVAL',
    'FALLING_TIME'
])

BombConfig = namedtuple('BombConfig', [
    'SPAWN_INTERVAL',
    'FALLING_TIME'
])


game_config = GameConfig(
    WIDTH=800,
    HEIGHT=400,
    FPS=60,
    BACKGROUND_COLOR='Black',
    TITLE='Fruit Ninja'
)

blade_config = BladeConfig(
    COLORS=['White'],
    VISIBILITY_DURATION=.2,
    INPUT_SOURCE=InputSource.FINGER
)

fruit_config = FruitConfig(
    SPAWN_INTERVAL=70,
    FALLING_TIME=2
)

bomb_config = BombConfig(
    SPAWN_INTERVAL=300,
    FALLING_TIME=2
)

global_config = GlobalConfig(
    game=game_config,
    blade=blade_config,
    fruit=fruit_config,
    bomb=bomb_config
)
