from src.app.utils.enums.enum_utils import ExtendedEnum


class ItemType(ExtendedEnum):
    PLAIN_FRUIT = 'PLAIN_FRUIT'
    FREEZE_FRUIT = 'FREEZE_FRUIT'
    GRAVITY_FRUIT = 'GRAVITY_FRUIT'
    BOMB = 'BOMB'


class PlainFruitType(ExtendedEnum):
    APPLE = 'apple'
    BANANA = 'banana'
    BASAHA = 'basaha'
    PEACH = 'peach'
    WATERMELON = 'watermelon'
