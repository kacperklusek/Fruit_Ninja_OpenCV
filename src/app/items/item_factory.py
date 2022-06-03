import random
from pygame.sprite import Group
from src.app.items.bomb import Bomb
from src.app.utils.enums import ItemType, FruitType, BonusType
from src.app.items.fruit import PlainFruit, FreezeFruit, GravityFruit, BonusFruitType


class ItemFactory:
    @staticmethod
    def create(item_type: ItemType, group: Group):
        match item_type:
            case ItemType.PLAIN_FRUIT:
                return ItemFactory.create_plain_fruit(group)
            case ItemType.BOMB:
                return ItemFactory.create_bomb(group)
            case ItemType.BONUS_FRUIT:
                return ItemFactory.create_bonus_fruit(group)

    @staticmethod
    def create_plain_fruit(group):
        fruit_type = random.choice(FruitType.values())
        return PlainFruit(fruit_type, group)

    @staticmethod
    def create_bomb(group):
        return Bomb(group)

    @staticmethod
    def create_bonus_fruit(group):
        item_type = random.choice(BonusType.names())
        match item_type:
            case BonusType.FREEZE.name:
                return FreezeFruit(BonusFruitType.FREEZE.value, group)
            case BonusType.GRAVITY.name:
                return GravityFruit(BonusFruitType.GRAVITY.value, group)
