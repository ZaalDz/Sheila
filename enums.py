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

    DEFAULT_WHEEL_POSITION = 'default_wheel_position'
    DEFAULT_CAMERA_POSITION = 'default_camera_position'

    CAMERA_UP = 'camera_up'
    CAMERA_DOWN = 'camera_down'


class CommandKeys(BaseEnum):

    MOVEMENT_TYPE = 'movement_type'
    SPEED = 'speed'
    MOVE_DURATION = 'duration'
    ROTATE_DURATION = 'rotate_duration'
    CAMERA_ROTATION_DEGREE = 'camera_rotation_degree'
    CAR_ROTATION_DEGREE = 'car_rotation_degree'
