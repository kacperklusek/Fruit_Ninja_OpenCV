import random
from pygame.sprite import Group
from src.app.utils.enums import ItemType, FruitType
from src.app.items.fruit import PlainFruit, GravityFruit, FreezeFruit
from src.app.items.bomb import Bomb


class ItemFactory:
    @staticmethod
    def create(item_type: ItemType, group: Group):
        match item_type:
            case ItemType.PLAIN_FRUIT:
                return ItemFactory.create_plain_fruit(group)
            case ItemType.BOMB:
                return ItemFactory.create_bomb(group)
            # case ItemType.FREEZE_FRUIT:
            #     return FreezeFruit()
            # case ItemType.GRAVITY_FRUIT:
            #     return GravityFruit()

    @staticmethod
    def create_plain_fruit(group):
        fruit_type = random.choice(FruitType.values())
        return PlainFruit(fruit_type, group)

    @staticmethod
    def create_bomb(group):
        return Bomb(group)
