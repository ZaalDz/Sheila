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

    FORWARD_LEFT = 'forward_left'
    FORWARD_RIGHT = 'forward_right'
    BACKWARD_LEFT = 'backward_left'
    BACKWARD_RIGHT = 'backward_right'

    CAMERA_UP = 'camera_up'
    CAMERA_DOWN = 'camera_down'


class CommandKeys(BaseEnum):
    MOVEMENT_TYPE = 'movement_type'
    MOVE_SPEED = 'speed'
    ROTATE_SPEED = 'rotate_speed'
    MOVE_DURATION = 'duration'
    ROTATE_DURATION = 'rotate_duration'
