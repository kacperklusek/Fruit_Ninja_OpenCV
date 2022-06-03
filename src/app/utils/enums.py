from enum import Enum, auto


class ExtendedEnum(Enum):
    @classmethod
    def names(cls):
        return [x.name for x in cls]

    @classmethod
    def values(cls):
        return [x.value for x in cls]


class ItemType(ExtendedEnum):  # TODO -maybe change all properties to auto()
    PLAIN_FRUIT = auto()
    BOMB = auto()
    BONUS_FRUIT = auto()


class BonusItemType(ExtendedEnum):
    FREEZE_FRUIT = auto()
    GRAVITY_FRUIT = auto()


class FruitType(ExtendedEnum):
    APPLE = 'apple'
    PEACH = 'peach'
    BANANA = 'banana'
    STRAWBERRY = 'strawberry'
    WATERMELON = 'watermelon'


class InputSource(Enum):
    FINGER = 'finger'
    HAND = 'hand'
    MOUSE = 'mouse'


class Orientation(Enum):
    HORIZONTAL = auto()
    VERTICAL = auto()


class GameMode(Enum):
    CLASSIC = auto()
    ARCADE = auto()
    ZEN = auto()
    CLASSIC_ATTACK = auto()
    ZEN_DUEL = auto()
