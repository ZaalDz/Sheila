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

    def move(self, *, forward=True):
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

    def rotate_wheel(self, *, left=False, right=False):
        """
        move wheel left, right or starting state, default value is starting state

        """

        car_rotation_degree = self.base_user_command[CommandKeys.CAR_ROTATION_DEGREE]

        if left:

            if car_rotation_degree > CarSettings.MIN_LEFT_TURN:
                self.base_user_command[CommandKeys.CAR_ROTATION_DEGREE] -= CarSettings.WHEEL_ROTATE_SPEED

            movement_type = MovementType.LEFT

        elif right:
            if car_rotation_degree < CarSettings.MAX_RIGHT_TURN:
                self.base_user_command[CommandKeys.CAR_ROTATION_DEGREE] += CarSettings.WHEEL_ROTATE_SPEED

            movement_type = MovementType.RIGHT
        else:
            self.base_user_command[CommandKeys.CAR_ROTATION_DEGREE] = CarSettings.STARTING_ROTATION_POSITION
            movement_type = MovementType.DEFAULT_WHEEL_POSITION

        rotate_command = {
            CommandKeys.MOVEMENT_TYPE: movement_type,
            CommandKeys.CAR_ROTATION_DEGREE: self.base_user_command[CommandKeys.CAR_ROTATION_DEGREE],
            CommandKeys.ROTATE_DURATION: self.base_user_command[CommandKeys.ROTATE_DURATION]
        }

        return rotate_command

    def rotate_camera(self, *, down=False, up=False):
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

    def build_commands(self, event_keys, *, set_wheel_default_position=False):

        if set_wheel_default_position:
            return [self.rotate_wheel()]

        command_list = []

        for each_event_key in event_keys:
            movement_type = movement_mapper.get(each_event_key)

            if movement_type == MovementType.LEFT:
                command = self.rotate_wheel(left=True)

            elif movement_type == MovementType.RIGHT:
                command = self.rotate_wheel(right=True)

            elif movement_type == MovementType.CAMERA_DOWN:
                command = self.rotate_camera(down=True)

            elif movement_type == MovementType.CAMERA_UP:
                command = self.rotate_camera(up=True)
            elif movement_type == MovementType.FORWARD:
                command = self.move()
            else:
                command = self.move(forward=False)

            command_list.append(command)
        return command_list


