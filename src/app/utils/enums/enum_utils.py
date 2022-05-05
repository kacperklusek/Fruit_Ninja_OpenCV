from enum import Enum


class ExtendedEnum(Enum):
    @classmethod
    def names(cls):
        return [x.name for x in cls]

    @classmethod
    def values(cls):
        return [x.value for x in cls]
