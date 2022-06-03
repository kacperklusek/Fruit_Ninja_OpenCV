from enum import Enum, auto


class ExtendedEnum(Enum):
    @classmethod
    def names(cls):
        return [x.name for x in cls]

    @classmethod
    def values(cls):
        return [x.value for x in cls]


class ItemType(ExtendedEnum):
    BOMB = auto()
    PLAIN_FRUIT = auto()
    BONUS_FRUIT = auto()


class FruitType(ExtendedEnum):
    APPLE = 'apple'
    PEACH = 'peach'
    BANANA = 'banana'
    STRAWBERRY = 'strawberry'
    WATERMELON = 'watermelon'


class BonusFruitType(ExtendedEnum):
    FREEZE = 'freeze-banana'
    GRAVITY = 'gravity-banana'


class BonusType(ExtendedEnum):
    FREEZE = auto()
    GRAVITY = auto()


class InputSource(ExtendedEnum):
    FINGER = 'finger'
    HAND = 'hand'
    MOUSE = 'mouse'


class Orientation(ExtendedEnum):
    HORIZONTAL = auto()
    VERTICAL = auto()


class GameMode(ExtendedEnum):
    CLASSIC = auto()
    ARCADE = auto()
    ZEN = auto()
    CLASSIC_ATTACK = auto()
    ZEN_DUEL = auto()
