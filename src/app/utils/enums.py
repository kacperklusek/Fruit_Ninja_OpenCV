from enum import Enum, auto


class ExtendedEnum(Enum):
    @classmethod
    def names(cls):
        return [x.name for x in cls]

    @classmethod
    def values(cls):
        return [x.value for x in cls]


class ItemType(ExtendedEnum):  # TODO -maybe change all properties to auto()
    PLAIN_FRUIT = 'PLAIN_FRUIT'
    FREEZE_FRUIT = 'FREEZE_FRUIT'
    GRAVITY_FRUIT = 'GRAVITY_FRUIT'
    BOMB = 'BOMB'


class PlainFruitType(ExtendedEnum):
    APPLE = 'apple'
    BANANA = 'banana'
    BASAHA = 'basaha'  # TODO - change to strawberry
    PEACH = 'peach'
    WATERMELON = 'watermelon'


class InputSource(Enum):
    FINGER = 'finger'
    HAND = 'hand'
    MOUSE = 'mouse'


class GameMode(ExtendedEnum):
    ZEN = 'Zen'
    CLASSIC = 'Classic'
    ARCADE = 'Arcade'
    MULTIPLAYER = 'Multiplayer'


class Orientation(Enum):
    HORIZONTAL = auto()
    VERTICAL = auto()
