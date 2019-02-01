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

    CAMERA_UP = 'camera_up'
    CAMERA_DOWN = 'camera_down'


class CommandKeys(BaseEnum):

    COMMAND_EXIST = 'command_exist'
    MOVEMENT_TYPE = 'movement_type'
    SPEED = 'speed'
    MOVE_DURATION = 'duration'
    ROTATE_DURATION = 'rotate_duration'
    CAMERA_ROTATION_DEGREE = 'camera_rotation_degree'
    CAR_ROTATION_DEGREE = 'car_rotation_degree'
