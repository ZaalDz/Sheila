from enum import Enum


class BaseEnum(str, Enum):
    def __str__(self):
        return f'{self.value}'

    def __get__(self, instance, owner):
        return self.value


class MovementType(BaseEnum):
    FORWARD = 'forward'
    BACKWARD = 'backward'
    LEFT = 'left'
    RIGHT = 'right'

    STOP = 'stop'


class CommandKeys(BaseEnum):
    COMMAND_TYPE = 'movement_type'
    MOVE_SPEED = 'speed'
    ROTATE_SPEED = 'rotate_speed'
    MOVE_DURATION = 'duration'
    ROTATE_DURATION = 'rotate_duration'
    DRIVER = 'driver'
    ACCURACY = 'accuracy'


class Driver(BaseEnum):
    AUTONOMOUS = 'autonomous'
    MANUAL = 'manual'
