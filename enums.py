from enum import Enum


class BaseEnum(str, Enum):
    def __str__(self):
        return f'{self.value}'

    def __get__(self, instance, owner):
        return self.value


class Directions(BaseEnum):
    FORWARD = 1
    BACKWARD = 2
    LEFT = 3
    RIGHT = 4


class CommandKeys(BaseEnum):
    DIRECTION = 10
    SPEED = 11
    DURATION = 12
