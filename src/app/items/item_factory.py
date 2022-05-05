import random
from src.app.utils.enums.items import ItemType, PlainFruitType
from src.app.items.fruit import PlainFruit
from src.app.items.bomb import Bomb


class ItemFactory:
    @staticmethod
    def create(item_type: ItemType):
        match item_type:
            case ItemType.PLAIN_FRUIT:
                return ItemFactory.create_plain_fruit()
            case ItemType.BOMB:
                return ItemFactory.create_bomb()
            case _:
                return PlainFruit('apple')  # TODO - add bonus fruits

    @staticmethod
    def create_plain_fruit():
        fruit_type = random.choice(PlainFruitType.values())
        return PlainFruit(fruit_type)

    @staticmethod
    def create_bomb():
        return Bomb()
