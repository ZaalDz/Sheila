from threading import Lock

from enums import MovementType, CommandKeys
from settings import CarSettings
from controller.singleton import Singleton

movement_mapper = {
    "'w'": MovementType.FORWARD,
    "'s'": MovementType.BACKWARD,
    "'a'": MovementType.LEFT,
    "'d'": MovementType.RIGHT,
    "'q'": MovementType.CAMERA_UP,
    "'z'": MovementType.CAMERA_DOWN
}


class CommandBuilder(metaclass=Singleton):

    def __init__(self):
        self.lock = Lock()

        self.base_user_command = {
            CommandKeys.MOVE_DURATION: CarSettings.MOVE_DURATION,
            CommandKeys.ROTATE_DURATION: CarSettings.ROTATE_DURATION,
            CommandKeys.SPEED: CarSettings.CAR_SPEED,
            CommandKeys.CAMERA_ROTATION_DEGREE: CarSettings.STARTING_CAMERA_POSITION,
            CommandKeys.CAR_ROTATION_DEGREE: CarSettings.STARTING_ROTATION_POSITION
        }

    def move(self, *, forward: bool = True) -> dict:
        """
        move car forward or backward, default value is forward

        """

        if forward:
            movement_type = MovementType.FORWARD
        else:
            movement_type = MovementType.BACKWARD

        move_command = {
            CommandKeys.MOVEMENT_TYPE: movement_type,
            CommandKeys.SPEED: self.base_user_command[CommandKeys.SPEED],
            CommandKeys.MOVE_DURATION: self.base_user_command[CommandKeys.MOVE_DURATION]
        }

        return move_command

    def rotate_left(self) -> dict:

        car_rotation_degree = self.base_user_command[CommandKeys.CAR_ROTATION_DEGREE]

        if car_rotation_degree > CarSettings.MIN_LEFT_TURN:
            self.base_user_command[CommandKeys.CAR_ROTATION_DEGREE] -= CarSettings.WHEEL_ROTATE_SPEED

        rotate_command = {
            CommandKeys.CAR_ROTATION_DEGREE: self.base_user_command[CommandKeys.CAR_ROTATION_DEGREE],
        }
        return rotate_command

    def rotate_right(self) -> dict:

        car_rotation_degree = self.base_user_command[CommandKeys.CAR_ROTATION_DEGREE]

        if car_rotation_degree < CarSettings.MAX_RIGHT_TURN:
            self.base_user_command[CommandKeys.CAR_ROTATION_DEGREE] += CarSettings.WHEEL_ROTATE_SPEED

        rotate_command = {
            CommandKeys.CAR_ROTATION_DEGREE: self.base_user_command[CommandKeys.CAR_ROTATION_DEGREE],
        }
        return rotate_command

    def two_command(self, forward: bool, left: bool) -> dict:

        right = not left
        backward = not forward

        left_command = self.rotate_left() if left else self.rotate_right()
        final_command = self.move() if forward else self.move(forward=False)
        final_command.update(left_command)

        if forward and left:
            movement_type = MovementType.FORWARD_LEFT
        elif forward and right:
            movement_type = MovementType.FORWARD_RIGHT

        elif backward and left:
            movement_type = MovementType.BACKWARD_LEFT
        else:
            movement_type = MovementType.BACKWARD_RIGHT

        final_command[CommandKeys.MOVEMENT_TYPE] = movement_type
        return final_command

    def rotate_camera(self, *, down: bool = False, up: bool = False) -> dict:
        """
        move camera up or down, default value is up

        """

        camera_rotation_degree = self.base_user_command[CommandKeys.CAMERA_ROTATION_DEGREE]

        if up:
            if camera_rotation_degree < CarSettings.MAX_CAMERA_POSITION:
                self.base_user_command[CommandKeys.CAMERA_ROTATION_DEGREE] += CarSettings.CAMERA_ROTATE_SPEED
            movement_type = MovementType.CAMERA_UP
        elif down:
            if camera_rotation_degree > CarSettings.MIN_CAMERA_POSITION:
                self.base_user_command[CommandKeys.CAMERA_ROTATION_DEGREE] -= CarSettings.CAMERA_ROTATE_SPEED

            movement_type = MovementType.CAMERA_DOWN
        else:
            self.base_user_command[CommandKeys.CAMERA_ROTATION_DEGREE] = CarSettings.STARTING_CAMERA_POSITION

            movement_type = MovementType.DEFAULT_CAMERA_POSITION

        camera_command = {
            CommandKeys.MOVEMENT_TYPE: movement_type,
            CommandKeys.CAMERA_ROTATION_DEGREE: self.base_user_command[CommandKeys.CAMERA_ROTATION_DEGREE],
            CommandKeys.ROTATE_DURATION: self.base_user_command[CommandKeys.ROTATE_DURATION]
        }

        return camera_command

    def build_commands(self, event_keys: list) -> dict:

        movement_types = set([movement_mapper.get(each_event_key) for each_event_key in event_keys])

        if len(movement_types) <= 1 and (MovementType.LEFT in movement_types or MovementType.RIGHT in movement_types):
            return {}

        if {MovementType.FORWARD, MovementType.RIGHT}.issubset(movement_types):
            command = self.two_command(forward=True, left=False)

        elif {MovementType.BACKWARD, MovementType.LEFT}.issubset(movement_types):
            command = self.two_command(forward=False, left=True)

        elif {MovementType.BACKWARD, MovementType.RIGHT}.issubset(movement_types):
            command = self.two_command(forward=False, left=False)
        elif {MovementType.FORWARD, MovementType.LEFT}.issubset(movement_types):
            command = self.two_command(forward=True, left=True)

        elif MovementType.BACKWARD in movement_types:
            command = self.move(forward=False)

        else:
            command = self.move(forward=True)

        return command

